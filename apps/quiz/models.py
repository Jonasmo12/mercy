from django.db import models
from django.utils.text import slugify
import random
from django.urls import reverse
from main.models import Teacher
from apps.section.models import (
    Section,
)
from main.models import (
    Subject,
    Student
)



class Quiz(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    numberOfQuestions = models.IntegerField(verbose_name="Number Of Questions")
    passScore = models.IntegerField(verbose_name="Pass Percentage")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    slug = models.SlugField(null=True)
    createdBy = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse('quiz:quizDetail', kwargs={'quizSlug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Quizess'

    def __str__(self):
        return f"{self.title}"

    def getQuestions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.numberOfQuestions]
    

class Result(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "{0}".format(self.score)


