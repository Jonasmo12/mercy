from django.urls import path, include
from .views import (
    HomeView,
    ProfileView,
    SubjectDetailView,
    SectionView,
    deleteEnrolmentView,

    EnrolDetailView,
)


app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('<str:pk>/', EnrolDetailView.as_view(), name='enrolment'),
    path('<str:pk>/delete', deleteEnrolmentView, name='deleteEnrolment'),
    path('<str:pk>/<str:id>/', SubjectDetailView.as_view(), name='subject'),
    path('<str:pk>/<str:id>/<str:sectionSlug>/', SectionView.as_view(), name='section'),
    path('<str:pk>/<str:id>/<str:sectionSlug>/', include('apps.quiz.urls', namespace='quiz')), 
]