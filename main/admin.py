from django.contrib import admin
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.conf import settings
import csv
from django.http import HttpResponse
from main.models import (
    Student, Subject, Enrol, Teacher
    )
from apps.section.models import Section
from apps.quiz.models import Quiz
from django import forms


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class SectionAdmin(admin.StackedInline):
    model = Section


class TeacherAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('full_Name', 'schoolID', 'date_joined')
    list_filter = ('date_joined', 'is_active', 'subject',)
    search_fields = ('email',)
    view_on_site = False
    actions = ["export_as_csv"]
    exclude = ('user_permissions', 'password', 'is_superuser', "is_student", "is_teacher",)

    def subject(self, obj):
        return ", ".join([subject.name for subject in obj.subject_set.all()])
        Subjects.short_description = "subjects"

    def get_readonly_fields(self, request, obj=None):
        """
            return as read only for teacher change view
        """
        if obj:
            return [
                "schoolID",
                "last_login", 
                "date_joined",
                # "groups",
                "is_active",
                "is_staff",  
                ]
        else:
            """
                return as read only during obj creation.
            """
            return [
                'createdBy',
                'groups',
                'last_login', 
                'date_joined',
                "is_active",
                "is_staff",
                ]
    
    def full_Name(self, obj):
        names = obj.title+". "+ obj.firstName + " " + obj.lastName
        return names

    def save_model(self, request, obj, form, change):
        """
            sends email to the created teacher, 
            none is sent during change of details.
        """
        if not change:
            print('added')
            obj.save()
            password = Teacher.objects.make_random_password()
            obj.set_password(password)
            group = Group.objects.get(name='teachers')
            obj.groups.add(group)
            obj.is_staff = True
            # obj.createdBy = request.user.administrator
            print(obj)

            name = request.POST.get('firstName')
            email = request.POST.get('email')
            schoolID = request.POST.get('schoolID')

            print(name, email, schoolID, password)

            send_mail(
                'Login Details - DISCERNDLearn',
                'Hi, ' + name + '. \n \n You were added a Teacher on DISCERNDLearn, please find your login details below \n \n' + 
                'schooldID: ' + schoolID + '.\n' + 
                'Password: ' + password + '. \n \n If you think this was a mistake please ignore the email.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            
            super(TeacherAdmin, self).save_model(request, obj, form, change)
        else:
            print('changed')
            super(TeacherAdmin, self).save_model(request, obj, form, change)
        super(TeacherAdmin, self).save_model(request, obj, form, change)


class FilterChildObjects(admin.ModelAdmin):
    """
        Filters content by teacher
    """
    def get_queryset(self, request):
        qs = super(FilterChildObjects, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(teacher=request.user.teacher)


class EnrolAdmin(admin.TabularInline):
    """
        Inline form for student for easy enrolment to subjects
    """
    model = Enrol
    

class EnrolAdminSite(admin.ModelAdmin):
    """
        Displaying of Enrol model in the admin site
    """
    list_display = ('student', 'created', 'subject', 'active')
    list_filter = ('created', 'active',)
    search_fields = ('student__firstName', 'student__lastName', 'student__schoolID')
    # autocomplete_fields = ['subject', 'student']


class StudentAdmin(admin.ModelAdmin):
    list_display = ('schoolID', 'full_Name', 'Subjects',)
    list_filter = ('is_active', 'date_joined', 'last_login',)
    search_fields = ('schoolID', 'firstName', 'lastName')
    inlines = [EnrolAdmin]
    view_on_site = False
    exclude = ('user_permissions', 'password', 'is_superuser', "is_student", "is_teacher",)


    def Subjects(self, obj):
        return ", ".join([subject.name for subject in obj.subjects.all()])
        Subjects.short_description = "Subjects"

    def get_readonly_fields(self, request, obj=None):
        """
            return as read only for student change view
        """
        if obj:
            return [
                "schoolID",
                "last_login", 
                "date_joined",
                "groups",
                "is_active",
                "is_staff",    
                ]
        else:
            """
                return as read only during obj creation.
            """
            return [
                'groups',
                'last_login', 
                'date_joined',
                "is_active",
                "is_staff",
                ]

    def full_Name(self, obj):
        names = obj.firstName + " " + obj.lastName
        return names

    def save_model(self, request, obj, form, change):
        """
            sends email to the created administrator, 
            none is sent during change of details.
        """
        if not change:
            print('added')
            obj.save()
            password = Student.objects.make_random_password()
            obj.set_password(password)
            group = Group.objects.get(name='students')
            obj.groups.add(group)
            print(obj)

            name = request.POST.get('firstName')
            email = request.POST.get('email')
            schoolID = request.POST.get('schoolID')

            print(name, email, schoolID, password)

            send_mail(
                'Login Details - DISCERNDLearn',
                'Hi, ' + name + '. \n \n You were added as a student on DISCERNDLearn, please find your login details below \n \n' + 
                'schooldID: ' + schoolID + '.\n' + 
                'Password: ' + password + '. \n \n If you think this was a mistake please ignore the email.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            
            super(StudentAdmin, self).save_model(request, obj, form, change)
        else:
            print('changed')
            super(StudentAdmin, self).save_model(request, obj, form, change)
        super(StudentAdmin, self).save_model(request, obj, form, change)


class SubjectAdmin(FilterChildObjects):
    """
        subject in admin site.
    """

    list_display = ('name', 'level',)
    # prepopulated_fields = {'slug': ('code',)}
    list_filter = ('level',)
    view_on_site = False
    # autocomplete_fields = ['teacher']
    

admin.site.register(Student, StudentAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Enrol, EnrolAdminSite)
admin.site.register(Teacher, TeacherAdmin)