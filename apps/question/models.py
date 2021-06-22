from django.db import models
import random
from main.models import (
    Subject
)
from apps.quiz.models import (
    Quiz
)


class Question(models.Model):
    text = models.CharField(max_length=150)
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)

    def getAnswers(self):
        return self.answer_set.all()


class Answer(models.Model):

    text = models.CharField(max_length=30)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} for {}'.format(self.text, self.question)

    
    

