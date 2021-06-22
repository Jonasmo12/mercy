from django.contrib import admin
from .models import (
    Question,
    Answer
)
from apps.quiz.models import (
    Quiz
)

class AnswerInline(admin.TabularInline):
    model = Answer
    view_on_site = False


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'created')
    list_filter = ('quiz', admin.RelatedOnlyFieldListFilter),
    view_on_site = False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "quiz":
            kwargs['queryset'] = Quiz.objects.filter(createdBy=request.user.teacher)
        return super(QuestionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)