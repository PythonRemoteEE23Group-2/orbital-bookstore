import pytest
from django.contrib.auth.models import User
from store.models import Book, Favorite, Category, Subcategory, User


@pytest.mark.django_db
def test_create_book():
    """Test the creation of a Book object"""
    category = Category.objects.create(name="Fiction")
    subcategory = Subcategory.objects.create(name="Sci-Fi", category=category)
    book = Book.objects.create(
        title="Dune",
        author="Frank Herbert",
        price=29.99,
        availability=True,
        subcategory=subcategory
    )
    assert book.id is not None
    assert book.title == "Dune"


@pytest.mark.django_db
def test_update_book():
    """Test updating a Book object"""
    category = Category.objects.create(name="Non-Fiction")
    subcategory = Subcategory.objects.create(name="Biography", category=category)
    book = Book.objects.create(
        title="Steve Jobs",
        author="Walter Isaacson",
        price=34.99,
        availability=True,
        subcategory=subcategory
    )
    book.title = "Steve Jobs: A Biography"
    book.save()
    updated_book = Book.objects.get(id=book.id)
    assert updated_book.title == "Steve Jobs: A Biography"


@pytest.mark.django_db
def test_delete_book():
    """Test deleting a Book object"""
    category = Category.objects.create(name="Non-Fiction")
    subcategory = Subcategory.objects.create(name="History", category=category)
    book = Book.objects.create(
        title="Sapiens",
        author="Yuval Noah Harari",
        price=19.99,
        availability=True,
        subcategory=subcategory
    )
    book_id = book.id
    book.delete()
    assert not Book.objects.filter(id=book_id).exists()


@pytest.mark.django_db
def test_add_book_to_favorites():
    """Test that a user can add a book to favorites"""
    user = User.objects.create_user(username="testuser", password="testpass")
    category = Category.objects.create(name="Fiction")
    subcategory = Subcategory.objects.create(name="Adventure", category=category)
    book = Book.objects.create(
        title="The Hobbit",
        author="J.R.R. Tolkien",
        price=12.99,
        availability=True,
        subcategory=subcategory
    )

    favorite = Favorite.objects.create(user=user, book=book)

    assert favorite.id is not None
    assert favorite.book.title == "The Hobbit"
    assert favorite.user.username == "testuser"

@pytest.mark.django_db
def test_mark_book_as_favorite():
    """Test that a user can mark a book as favorite and it persists"""
    user = User.objects.create_user(username="testuser", password="testpass")
    category = Category.objects.create(name="Fiction")
    subcategory = Subcategory.objects.create(name="Adventure", category=category)
    book = Book.objects.create(
        title="The Hobbit",
        author="J.R.R. Tolkien",
        price=12.99,
        availability=True,
        subcategory=subcategory
    )

    Favorite.objects.create(user=user, book=book)

    assert Favorite.objects.filter(user=user, book=book).exists()
