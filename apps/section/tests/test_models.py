import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db
from ..models import (
    Section
)
from main.models import (
    Teacher,
    Teacher,
    Subject
)


class TestSection:
    def test_model(self):
        obj = mixer.blend('section.Section', pk=500)
        assert obj.pk == 500, 'should return instatnce of section'
    
    def test_url(self):
        obj = mixer.blend('section.Section', pk=500, url="httpp://jonas.com")
        assert obj.url == "httpp://jonas.com", 'returns url field'
    
    def test_teacher(self):
        teacher = mixer.blend(Teacher, firstName="James", lastName="Vidal", schoolID=1234512345)
        obj = mixer.blend('section.Section', pk=500, teacher=teacher)
        assert isinstance(obj.teacher, Teacher), 'should return instatnce of teacher'

    def test_subject(self):
        subject = mixer.blend(Subject, name="Accounting")
        obj = mixer.blend('section.Section', pk=500, subject=subject)
        assert isinstance(obj.subject, Subject), 'should return true'

    # def test_video(self):
    #     obj = mixer.blend('section.Section', pk=500)
    #     assert isinstance(obj.videoURL, Section)