from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm
)
from django.utils.translation import gettext_lazy as _
from django.forms import Textarea, CharField, ImageField, DateInput, CheckboxInput
from django.core.exceptions import ValidationError
from main.models import (
    Student,
    Subject,
    Teacher,
    Enrol,
)

class EnrolForm(forms.ModelForm):
    class Meta:
        model = Enrol
        fields = ('subject',)

    def __init__(self, student, *args, **kwargs):
        super(EnrolForm, self).__init__(*args, **kwargs)

        # shows a list of subject a student has not enrolled in, 
        # this block of code extends to a main.view.py file by adding request.user.student in get/post form
        
        self.fields['subject'].queryset = Subject.objects.exclude(enrol__student=student)


class TeacherCreationForm(UserCreationForm):
    bio= forms.CharField(widget= forms.Textarea(attrs={'placeholder':'Brag about yourself...'}))

    class Meta:
        model = Teacher
        fields = ('title', 'firstName', 'lastName', 'subject', 'bio', 'email', 'password1', 'password2')




class StudentCreationForm(UserCreationForm):

    class Meta:
        model = Student
        fields = ('firstName', 'lastName', 'schoolID', 'email', 'password1', 'password2')
        # widgets = {
        #     'dateOfBirth': DateInput(attrs={'type': 'date'})
        # }

    def clean(self):
        cleaned_data = super(StudentCreationForm, self).clean()
        # identityNumber = cleaned_data.get('identityNumber')
        # dateOfBirth = cleaned_data.get('dateOfBirth')

        # if len(identityNumber) != 13:
        #     self.add_error(
        #         'identityNumber', _('Please enter a valid South African Identity Number')
        #     )
        # if identityNumber[2:9] != dateOfBirth:
        #     self.add_error(
        #         'dateOfBirth', _('Identity Number and Date Of Birth do not match')
        #     )

        return cleaned_data