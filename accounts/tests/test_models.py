import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db
from ..models import Account


class TestAccount:
    def test_model(self):
        obj = mixer.blend("accounts.Account")
        assert obj.pk == 1, 'returns accounts pk'

    def test_activeStatus(self):
        obj = mixer.blend("accounts.Account")
        assert obj.is_active == True, 'returns obj status'

    def test_createuser(self):
        obj = Account.objects.create_user(schoolID=1234512345, email="james@mail.com", password=None)
        assert obj.pk == 1, 'returns created user object'
        # assert obj.schoolID == 1234512345, 'returns schoolID'
        # assert obj.email == "james@mail.com", 'returns email of user'
    
    def test_activeStatusOfUser(self):
        obj = Account.objects.create_user(schoolID=1234512345, email="james@mail.com", password=None)
        assert obj.is_active == True, 'should return true for is active'

    def test_createsuperuser(self):
        obj = Account.objects.create_superuser(schoolID=1234567890, email="super@email.com", password=None)
        assert obj.pk == 1, 'returns created superuser'

    def test_superUserStatus(self):
        obj = Account.objects.create_superuser(schoolID=1234567890, email="super@email.com", password=None)
        assert obj.is_superuser == True, 'should return superuser status'
    
    def test_staffStatus(self):
        obj = Account.objects.create_superuser(schoolID=1234567890, email="super@email.com", password=None)
        assert obj.is_staff == True, 'Should return is staff status'

    def test_str(self):
        obj = mixer.blend("accounts.Account", firstName="Jamie", lastName="Moloto", schoolID=1234512345)
        result = obj.__str__()
        assert result == "Jamie Moloto, 1234512345", 'returns str method of account'