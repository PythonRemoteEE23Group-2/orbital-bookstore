import pytest
from store.models import Book, Category, Subcategory
from django.urls import reverse


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
def test_read_book():
    """Test reading a Book object"""
    category = Category.objects.create(name="Fiction")
    subcategory = Subcategory.objects.create(name="Fantasy", category=category)
    book = Book.objects.create(
        title="Harry Potter",
        author="J.K. Rowling",
        price=24.99,
        availability=True,
        subcategory=subcategory
    )
    retrieved_book = Book.objects.get(id=book.id)
    assert retrieved_book.title == "Harry Potter"


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
def test_list_books():
    """Test listing all Book objects"""
    category = Category.objects.create(name="Fiction")
    subcategory1 = Subcategory.objects.create(name="Thriller", category=category)
    subcategory2 = Subcategory.objects.create(name="Romance", category=category)
    Book.objects.create(
        title="Gone Girl",
        author="Gillian Flynn",
        price=14.99,
        availability=True,
        subcategory=subcategory1
    )
    Book.objects.create(
        title="Pride and Prejudice",
        author="Jane Austen",
        price=10.99,
        availability=True,
        subcategory=subcategory2
    )
    books = Book.objects.all()
    assert len(books) == 2
    assert books[0].title == "Gone Girl"
    assert books[1].title == "Pride and Prejudice"
