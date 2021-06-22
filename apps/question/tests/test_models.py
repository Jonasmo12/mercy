import pytest
from mixer.backend.django import mixer
from ..models import (
    Question,
    Answer,
)
from apps.quiz.models import (
    Quiz,
)
pytestmark = pytest.mark.django_db


class TestQuestion:
    def test_model(self):
        obj = mixer.blend(Question, pk=100)
        assert obj.pk == 100, 'return question instance'

    def test_quizInstance(self):
        quiz = mixer.blend(Quiz, title="numbers")
        obj = mixer.blend(Question, pk=100, quiz=quiz)
        assert isinstance(obj.quiz, Quiz), "should return instance of quiz"
        assert obj.quiz.title == "numbers", "should return title of a quiz"


class TestAnswer:
    def test_model(self):
        obj = mixer.blend(Answer, pk=5)
        assert obj.pk == 5, 'return answer instance'

    def test_questionInstance(self):
        question = mixer.blend(Question, text="What is x?")
        obj = mixer.blend(Answer, pk=5, question=question)
        assert isinstance(obj.question, Question), "should true, question is instance in answer"
        assert obj.question.text == "What is x?", "should return question"