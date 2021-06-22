from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from ..views import (
    HomeView,
    SubjectDetailView,
    SectionView,
)


# class TestHomeView:
#     def test_anonymous(self):
        
#         request = RequestFactory().get('/')
#         request.user.student = AnonymousUser()
#         response = HomeView.as_view()(request)
#         assert response.status_code == 404, "should not be called by anyone"











