from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)
from django.core.paginator import Paginator
from django.db.models import (
    Min,
    Max,
    Avg,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import (
    View,
    DetailView,
)
from django.core import serializers
from django.http import (
    JsonResponse,
)
import datetime
from main.models import (
    Subject,
    Student,
    Enrol
)
from apps.section.models import Section
from apps.quiz.models import (
    Quiz,
    Result
)
from main.forms import EnrolForm


class HomeView(View):
    template_name = 'home.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                form = EnrolForm(request.user.student)
                student = request.user.student
                enrol = Enrol.objects.filter(student=student)    
                context = {'form': form, 'enrol': enrol}   
                return render(request, self.template_name, context)

            except Student.DoesNotExist:
                return redirect('/discerndlearn-staff/')

            return render(request, self.template_name)

        else:
            context = {}
            return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = EnrolForm(request.user.student, request.POST)
            if form.is_valid():
                enrol = form.save(commit=False)
                enrol.active = True
                enrol.student = request.user.student
                enrol.save()
                return redirect('/')
            
        context = {'form': form}
        return render(request, self.template_name, context)


class ProfileView(LoginRequiredMixin, View):
    template_name = 'profile.html'

    def get(self, request):
        student = request.user.student
        context = {'student': student}
        return render(request, self.template_name, context)


class EnrolDetailView(LoginRequiredMixin, View):
    context_object_name = 'enrol'
    model = Enrol
    queryset = Enrol.objects.all()
    template_name = 'main/enrol_detail.html'
    pk_url_kwarg = 'pk'

    def get(self, request, pk):
        enrol = self.model.objects.get(pk=pk)
        # calls a subject object from the enrol object
        # enrol is a child of subject, and it is used as an intermediery of subject and student.
        subject = enrol.subject
        print(subject.id)
        context = {'enrol': enrol, 'subject': subject}
        return render(request, self.template_name, context)


def deleteEnrolmentView(request, pk):
    enrol = Enrol.objects.get(pk=pk)

    if request.method == "POST":
        enrol.delete()
        return redirect("/")

    context = {"enrol": enrol}
    return render(request, 'main/forms/delete_subject.html', context)


class SubjectDetailView(LoginRequiredMixin, View):
    model = Subject
    queryset = Subject.objects.all()
    template_name = 'main/subject.html'

    def get(self, request, pk, id):
        enrol = Enrol.objects.get(pk=pk)
        subject = self.model.objects.get(id=id)
        sections = Section.objects.filter(subject=subject)
        paginator = Paginator(sections, 3) # Show 3 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'subject': subject,
            'page_obj': page_obj,
            'sections': sections,
            'enrol': enrol
        }
        return render(request, self.template_name, context)


class SectionView(LoginRequiredMixin, DetailView):
    context_object_name = 'section'
    template_name = 'main/section.html'
    model = Section
    queryset = Section.objects.all()
    pk_url_kwarg = 'sectionSlug'

    def get(self, request, pk, id, sectionSlug, *args, **kwargs):
        enrol = Enrol.objects.get(pk=pk)
        subject = Subject.objects.get(id=id)
        section = Section.objects.get(slug=sectionSlug)
        quiz = section.quiz_set.all()

        context = {'enrol': enrol, 'subject': subject, 'section': section, 'quiz': quiz}
        return render(request, self.template_name, context)