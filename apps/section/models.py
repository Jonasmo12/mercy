from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from main.models import Subject, Teacher


class Section(models.Model): 
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    video = models.URLField(blank=True)
    pdf = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=False, null=True)
    
    def sectionQuiz(self):
        quiz = self.quiz_set.all()
        return quiz

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('section:section', kwargs={'sectionSlug': self.slug})

    def shortDescription(self):
        queryset = self.description[:50]
        return queryset

    def __str__(self):
        return f"{self.title}"


