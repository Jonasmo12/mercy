import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db
from ..models import (
    Teacher,
    Student
)


class TestTeacher:
    
    def test_teacherModel(self):
        obj = mixer.blend('main.Teacher')
        assert obj.pk == 1, 'should return teacher instance'


class TestStudent:
    def test_model(self):
        obj = mixer.blend('main.Student')
        assert obj.pk == 1, 'should return student instance'
        

# class TestSubject:
#     def test_model(self):
#         obj = mixer.blend('main.Subject', pk=10000)
#         assert obj.pk == 10000, 'returns subject instance'

#     def test_saveForSlug(self):
#         obj = mixer.blend('main.Subject', pk=10000, name="Mathematics")
#         assert obj.slug == "mathematics", 'returns slug as lowercase name of subject'

#     def test_m2m(self):
#         student = mixer.blend('main.Student', firstName="Ago", lastName="Moloto", schoolID=1234512345)
#         obj = mixer.blend('main.Subject', name="Mathematics", students=student)
#         students = list(obj.students.values())
#         assert student.firstName == "Ago", 'should return students with relation to subject, m2m'

#     def test__str__(self):
#         obj = mixer.blend('main.Subject', name="Mathematics")
#         assert obj.__str__() == "Mathematics", 'returns subject __str__ method'

#     def test_save(self):
#         obj = mixer.blend('main.Subject', name="mathematics")
#         assert obj.slug == "mathematics", 'returns result of save method'


# class TestEnrol:
#     def test_model(self):
#         obj = mixer.blend('main.Enrol', pk=1)
#         assert obj.pk == 1, 'return enrol instance'

#     def test_student(self):
#         student = mixer.blend('main.Student', firstName="Ago", lastName="Moloto", schoolID=1234512345)
#         obj = mixer.blend('main.Enrol', pk=1, student=student)
#         assert isinstance(obj.student, Student), 'should return true for instance of a student'
