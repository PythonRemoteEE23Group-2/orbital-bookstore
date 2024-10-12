import pytest
from store.models import Book, Category, Subcategory, Favorite
from django.contrib.auth import get_user_model

User = get_user_model()


# Test creating a new book.
@pytest.mark.django_db
def test_create_book():
    # Create a category and subcategory for the book.
    category = Category.objects.create(name="Fiction")
    subcategory = Subcategory.objects.create(name="Science Fiction", category=category)

    # Create a new book object.
    book = Book.objects.create(
        title="Dune",
        author="Frank Herbert",
        price=14.99,
        availability=True,
        subcategory=subcategory
    )

    # Assert that the book has been created and exists in the database.
    assert Book.objects.filter(title="Dune").exists()
    assert book.author == "Frank Herbert"


# Test updating a book's information.
@pytest.mark.django_db
def test_update_book():
    # Create a category and subcategory for the book.
    category = Category.objects.create(name="Biography")
    subcategory = Subcategory.objects.create(name="Science", category=category)

    # Create a new book object.
    book = Book.objects.create(
        title="Elon Musk",
        author="Ashlee Vance",
        price=24.99,
        availability=True,
        subcategory=subcategory
    )

    # Update the book's title.
    book.title = "Steve Jobs: A Biography"
    book.save()

    # Retrieve the updated book and verify that the title has changed.
    updated_book = Book.objects.get(id=book.id)
    assert updated_book.title == "Steve Jobs: A Biography"


# Test deleting a book.
@pytest.mark.django_db
def test_delete_book():
    # Create a category and subcategory for the book.
    category = Category.objects.create(name="Non-Fiction")
    subcategory = Subcategory.objects.create(name="History", category=category)

    # Create a new book object.
    book = Book.objects.create(
        title="Sapiens",
        author="Yuval Noah Harari",
        price=19.99,
        availability=True,
        subcategory=subcategory
    )

    # Store the book's ID and then delete the book.
    book_id = book.id
    book.delete()

    # Assert that the book no longer exists in the database.
    assert not Book.objects.filter(id=book_id).exists()


# Test marking a book as favorite.
@pytest.mark.django_db
def test_mark_book_as_favorite():

    # Create a user and a book.
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

    # Mark the book as a favorite for the user.
    Favorite.objects.create(user=user, book=book)

    # Assert that the favorite relationship exists in the database.
    assert Favorite.objects.filter(user=user, book=book).exists()