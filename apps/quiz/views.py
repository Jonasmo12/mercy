from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.views.generic import (
    View,
    ListView,
    DetailView
)
from django.http import JsonResponse
import json
from django.db.models import Max
from apps.quiz.models import (
    Quiz,
    Result,
)
from apps.question.models import (
    Question,
    Answer,
)
from main.models import Student, Subject, Enrol
from apps.section.models import Section


class QuizView(DetailView):
    context_object_name = 'quiz'
    template_name = 'quiz/quiz.html'
    model = Quiz
    queryset = Quiz.objects.all()
    pk_url_kwarg = 'quizSlug'

    def get(self, request, pk, id, sectionSlug, quizSlug, *args, **kwargs):
        enrol = Enrol.objects.get(pk=pk)
        subject = Subject.objects.get(id=id)
        section = Section.objects.get(slug=sectionSlug)
        quiz = Quiz.objects.get(slug=quizSlug)
        student = request.user.student
        result = quiz.result_set.filter(student=student).aggregate(Max('score'))['score__max']
        context = {'enrol': enrol, 'subject': subject, 'section': section, 'quiz': quiz, 'result': result}
        return render(request, self.template_name, context)
    

def quizDataView(request, pk, id, sectionSlug, quizSlug):
    enrol = Enrol.objects.get(pk=pk)
    subject = Subject.objects.get(id=id)
    section = Section.objects.get(slug=sectionSlug)
    quiz = Quiz.objects.get(slug=quizSlug)

    questions = []
    for q in quiz.getQuestions():
        answers = []
        for a in q.getAnswers():
            answers.append(a.text)
        questions.append({str(q): answers})
    
    return JsonResponse({
        'data': questions
    })


def quizSaveView(request, pk, id, sectionSlug, quizSlug):

    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists()) # converting data to normal dict
        data_.pop('csrfmiddlewaretoken') # remove csrfmiddlewaretoken

        """ Query questions with the data"""
        for k in data_.keys(): 
            print('key: ', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        
        student = request.user.student
        enrol = Enrol.objects.get(pk=pk)
        subject = Subject.objects.get(id=id)
        section = Section.objects.get(slug=sectionSlug)
        quiz = Quiz.objects.get(slug=quizSlug)
        score = 0
        multiplier = 100 / quiz.numberOfQuestions
        results = []
        correctAnswer = None

        for q in questions: # get questions from the data
            a_selected = request.POST.get(q.text) # asign selected answeres to questions
            
            if a_selected != "": # checks wheather the answer is not blank
                question_answers = Answer.objects.filter(question=q) # assigns selected answers to the ansere model
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correctAnswer = a.text
                    else:
                        if a.correct:
                            correctAnswer = a.text
                results.append({str(q): {'correctAnswer': correctAnswer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})

        score_ = score * multiplier  
        Result.objects.create(quiz=quiz, student=student, score=score_, section=section, subject=subject)

        if score_ >= quiz.passScore:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})
