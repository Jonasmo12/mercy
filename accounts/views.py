from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.models import Group
import json
from django.http import (
    JsonResponse,
)
from django.core.mail import send_mail
from main.forms import StudentCreationForm, TeacherCreationForm
from .decorators import unauthenticatedUser
from main.models import Student, Teacher, Subject

def updateEmail(request):

    context = {}
    return render(request, '', context)


@unauthenticatedUser
def signUpStudentView(request):
    form = StudentCreationForm()
    if request.method == "POST":
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.is_student = True
            student.save()

            user = form.cleaned_data.get('email')
            name = form.cleaned_data.get('firstName')
            schoolID = form.cleaned_data.get('schoolID')

            print(name, user, schoolID)

            send_mail(
                'School ID - MERCY .',
                'Hi, ' + name + '. \n \n Thank you for signing up, please find your MERCY . school ID below \n \n' + 
                'schoold ID: ' + schoolID + '.\n \n' + 
                'If you think this was a mistake please ignore the email. \n \n' + 
                'mercy-learn.herokuapp.com',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            messages.success(request, 'School ID has been sent to ' + user + ' for varification purposes.')


            return redirect('accounts:login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticatedUser
def signUpTeacherView(request):
    subjects = Subject.objects.all()
    form = TeacherCreationForm()
    if request.method == "POST":
        form = TeacherCreationForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.is_teacher = True
            teacher.is_staff = True
            teacher.save()


            group = Group.objects.get(name='teachers')
            teacher.groups.add(group)

            user = form.cleaned_data.get('email')
            name = form.cleaned_data.get('firstName')
            schoolID = form.cleaned_data.get('schoolID')

            print(name, user, schoolID)

            # send_mail(
            #     'Login Details - DISCERNDLearn',
            #     'Hi, ' + name + '. \n \n You were added as a student on DISCERNDLearn, please find your login details below \n \n' + 
            #     'schooldID: ' + schoolID + '.\n' + 
            #     'Password: ' + password + '. \n \n If you think this was a mistake please ignore the email.',
            #     settings.EMAIL_HOST_USER,
            #     [email],
            #     fail_silently=False,
            # )

            messages.success(request, 'School ID has been sent to ' + user + ' for varification purposes.')

            return redirect('accounts:login')

    context = {
        'form': form,
        'subjects': subjects,
        }
    return render(request, 'accounts/register.html', context)



@unauthenticatedUser
def loginView(request):
    if request.method == "POST":
        schoolID = request.POST.get('schoolID')
        password = request.POST.get('password')

        user = authenticate(request, schoolID=schoolID, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:home')
        else:
            messages.info(
                request, 'Password is case sensitive and/or password does not match schoolID')

    return render(request, 'accounts/login.html')


def logoutView(request):
    logout(request)
    return redirect('/')


