from django import forms
from question.models import (
    Question,
    Choice
)


class MultipleChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('choice_text',)