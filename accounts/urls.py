from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
)
from .views import (
    signUpStudentView,
    signUpTeacherView,
    loginView,
    logoutView,
)

app_name = 'accounts'

urlpatterns = [
    path('student/', signUpStudentView, name='registerStudent'),
    path('teacher/', signUpTeacherView, name='registerTeacher'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),


    
    #  password management urls
    
    path('password/reset/', PasswordResetView.as_view(template_name='accounts/password/password_reset.html'), name='reset_password'),
    path('password/reset/confirmation/', PasswordResetDoneView.as_view(template_name='accounts/password/password_confirmation.html'), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password/password_reset_form.html'), name='password_reset_confirm'),
    path('password/reset/complete', PasswordResetCompleteView.as_view(template_name='accounts/password/password_login.html'), name='password_reset_complete'),

]
