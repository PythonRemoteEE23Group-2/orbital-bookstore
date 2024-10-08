import pytest
from store.models import User
from django.contrib.auth import authenticate


@pytest.mark.django_db
def test_create_user():
    """Test creating a new user"""
    user = User.objects.create_user(username="testuser", password="testpass", email="testuser@example.com")
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"


@pytest.mark.django_db
def test_read_user():
    """Test reading a user's details"""
    user = User.objects.create_user(username="readuser", password="readpass", email="readuser@example.com")
    retrieved_user = User.objects.get(id=user.id)
    assert retrieved_user.username == "readuser"
    assert retrieved_user.email == "readuser@example.com"


@pytest.mark.django_db
def test_update_user():
    """Test updating a user's profile"""
    user = User.objects.create_user(username="updateuser", password="updatepass", email="updateuser@example.com")
    user.email = "newemail@example.com"
    user.save()

    updated_user = User.objects.get(id=user.id)
    assert updated_user.email == "newemail@example.com"


@pytest.mark.django_db
def test_delete_user():
    """Test deleting a user"""
    user = User.objects.create_user(username="deleteuser", password="deletepass", email="deleteuser@example.com")
    user_id = user.id
    user.delete()

    assert not User.objects.filter(id=user_id).exists()


@pytest.mark.django_db
def test_authenticate_user():
    """Test authenticating a user"""
    user = User.objects.create_user(username="authuser", password="authpass", email="authuser@example.com")
    authenticated_user = authenticate(username="authuser", password="authpass")

    assert authenticated_user is not None
    assert authenticated_user.username == "authuser"
