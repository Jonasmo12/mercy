from django.contrib import admin
from django.db.models import Max, Min, Avg
from django.urls import path, reverse
from django import forms
from apps.quiz.models import (
    Quiz,
    Result
)
from main.models import (
    Teacher,
    Subject,

)
from apps.section.models import (
    Section
)
from main.admin import ExportCsvMixin


class SubjectsSimpleFilter(admin.SimpleListFilter):
    title = 'Subjects'
    parameter_name = 'subjects'

    def lookups(self, request, model_admin):
        listOfSubjects = []
        queryset = Subject.objects.filter(teacher=request.user.teacher)
        for subject in queryset:
            listOfSubjects.append(
                (str(subject.id), (subject.name, subject.level))
            )
        return listOfSubjects

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value to decide how to filter the queryset.
        if self.value():
            return queryset.filter(subject_id=self.value())
        return queryset

class FilterTeacherobjects(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(FilterTeacherobjects, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(createdBy=request.user.teacher)


class FilterResultsByTeacher(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(FilterResultsByTeacher, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(subject__teacher=request.user.teacher)


class ResultDisplay(FilterResultsByTeacher, ExportCsvMixin):
    list_display = ('student', 'quiz', 'section', 'subject', 'score', )
    list_filter = ('section', admin.RelatedOnlyFieldListFilter),
    # readonly_fields = ('student', 'quiz', 'section', 'score', 'subject',)
    search_fields = ('subject__name', 'subject__grade',)
    actions = ["export_as_csv"]

    def score(self, obj):
        firstScore = obj.score.first()
        return firstScore


class ResultAdmin(admin.TabularInline):
    model = Result

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuizAdmin(FilterTeacherobjects, ExportCsvMixin):
    list_display = ('title', 'section', 'subject', 'created')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = (SubjectsSimpleFilter, 'created',)
    search_fields = ('title',)
    view_on_site = False
    actions = ["export_as_csv"]
    readonly_fields = ('createdBy',)

    def queryset(self, request):
        qs = super(QuizAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(teacher=request.user.teacher)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'subject':
            kwargs['queryset'] = Subject.objects.filter(teacher=request.user.teacher)
        elif db_field.name == 'section':
            kwargs['queryset'] = Section.objects.filter(teacher=request.user.teacher)
        return super(QuizAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        obj.createdBy = request.user.teacher
        super().save_model(request, obj, form, change)
       
    inlines = [ResultAdmin]


admin.site.register(Result, ResultDisplay)
admin.site.register(Quiz, QuizAdmin)