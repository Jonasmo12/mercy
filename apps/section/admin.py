from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy as _
from apps.section.models import Section
from main.models import (
    Subject,
)

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
        return qs.filter(teacher=request.user.teacher)


class SectionAdmin(FilterTeacherobjects):
    list_display = ('title', 'subject', 'created_at', 'update_at',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = (SubjectsSimpleFilter, 'created_at', 'update_at')
    search_fields = ('title',)

    def get_readonly_fields(self, request, obj=None):
        """
            return as read only for change view
        """
        if obj:
            return [
                "teacher",    
                ]
        else:
            """
                return as read only during obj creation.
            """
            return [
                'teacher',
                ]                

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject":
            kwargs['queryset'] = Subject.objects.filter(teacher=request.user.teacher)
        return super(SectionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


    def save_model(self, request, obj, form, change):
        obj.teacher = request.user.teacher
        super(SectionAdmin, self).save_model(request, obj, form, change)


admin.site.register(Section, SectionAdmin)