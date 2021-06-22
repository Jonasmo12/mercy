from django.urls import path
from apps.quiz.views import (
    QuizView,
    quizSaveView,
    quizDataView,
)


app_name = 'quiz'

urlpatterns = [
    #path('list/', QuizListView.as_view(), name='quizList'),
    path('<str:quizSlug>/', QuizView.as_view(), name='quizDetail'),
    path('<str:quizSlug>/save/', quizSaveView, name='quizSave'),
    path('<str:quizSlug>/data/', quizDataView, name='quizData'),
]