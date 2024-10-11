import pytest
from django.db import IntegrityError
from store.models import Folk  # Assuming the model is in 'store' app


@pytest.mark.django_db  # Required for database interaction in pytest-django
def test_create_folk():
    """
    Test creating a Folk entry in the database.
    """
    folk = Folk.objects.create(name="Alice", email="alice@example.com")

    assert folk.id is not None  # Ensures that the Folk entry was created and has an ID
    assert folk.name == "Alice"  # Name is correctly set
    assert folk.email == "alice@example.com"  # Email is correctly set


@pytest.mark.django_db
def test_read_folk():
    """
    Test reading a Folk entry from the database.
    """
    Folk.objects.create(name="Bob", email="bob@example.com")

    folk = Folk.objects.get(email="bob@example.com")

    assert folk.name == "Bob"  # Correct Folk entry is retrieved
    assert folk.email == "bob@example.com"  # Email matches


@pytest.mark.django_db
def test_update_folk():
    """
    Test updating a Folk entry in the database.
    """
    folk = Folk.objects.create(name="Charlie", email="charlie@example.com")

    folk.name = "Charles"  # Change the name
    folk.save()  # Save the updated entry

    updated_folk = Folk.objects.get(email="charlie@example.com")

    assert updated_folk.name == "Charles"  # The name should be updated


@pytest.mark.django_db
def test_delete_folk():
    """
    Test deleting a Folk entry from the database.
    """
    folk = Folk.objects.create(name="David", email="david@example.com")

    folk_id = folk.id
    folk.delete()  # Delete the Folk entry

    # Confirm that the entry no longer exists
    with pytest.raises(Folk.DoesNotExist):
        Folk.objects.get(id=folk_id)


@pytest.mark.django_db
def test_read_non_existent_folk():
    """
    Test that trying to read a non-existent Folk raises a DoesNotExist exception.
    """
    with pytest.raises(Folk.DoesNotExist):
        Folk.objects.get(email="nonexistent@example.com")
