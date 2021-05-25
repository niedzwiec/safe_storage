import pytest
from django.test import Client
from django.urls import reverse

from accounts.models import User
from safe_storage.models import Storage

from uuid import UUID

def validate_uuid4(uuid_string):
    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
         return False

    return val.hex == uuid_string.replace('-','')

@pytest.fixture
def storage():
    s = Storage.objects.create(url='https://wp.pl')
    password = s.generate_password()
    s.save()
    return s, password

@pytest.fixture
def user():
    u = User.objects.create(username='cooklee')
    return u


@pytest.mark.django_db
def test_if_login_req_add_to_storage():
    c = Client()
    response = c.get(reverse('add_to_storage'))
    assert response.status_code == 302
    assert response.url.startswith('/accounts/login/?next=/safe_storage/')

@pytest.mark.django_db
def test_add_to_storage(user):
    c = Client()
    c.force_login(user)
    response = c.post(reverse('add_to_storage'), {'url':'https://wp.pl'}, headers={'HTTP_USER_AGENT':'abc'})
    assert response.status_code == 200
    assert validate_uuid4(response.context['storage'].slug)
    assert hash(response.context['password']) == response.context['storage'].password

