from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from store.models import Book, Category, Subcategory, Cart, CartItem, Review


# This test case class contains tests for different views in the store app.
class ViewsTestCase(TestCase):

    # setUp method to create the necessary data before each test case runs.
    def setUp(self):
        # Create a test client to simulate requests.
        self.client = Client()

        # Create a test user for login purposes.
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create a category and subcategory for the book.
        self.category = Category.objects.create(name='Test Category')
        self.subcategory = Subcategory.objects.create(name='Test Subcategory', category=self.category)

        # Create a book object that will be used in multiple tests.
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            price=9.99,
            subcategory=self.subcategory
        )

    # Test for the home view, which lists books and categories.
    def test_home_view(self):
        # Simulate a GET request to the home page.
        response = self.client.get(reverse('home'))

        # Check if the response has an HTTP status code of 200 (OK).
        self.assertEqual(response.status_code, 200)

        # Verify that the home page uses the correct template.
        self.assertTemplateUsed(response, 'store/home.html')

        # Check that the response contains the 'books' and 'categories' in its context.
        self.assertIn('books', response.context)
        self.assertIn('categories', response.context)

    # Test for adding a book to the cart.
    def test_add_to_cart_view(self):
        # Log in as the test user.
        self.client.login(username='testuser', password='testpass123')

        # Simulate a POST request to add the book to the cart.
        response = self.client.post(reverse('add_to_cart', args=[self.book.id]))

        # Check that the user is redirected to the cart view after adding the book.
        self.assertRedirects(response, reverse('view_cart'))

        # Retrieve the cart for the user.
        cart = Cart.objects.get(user=self.user)

        # Verify that the cart contains one item.
        self.assertEqual(cart.items.count(), 1)

        # Confirm that the item in the cart is the correct book.
        self.assertEqual(cart.items.first().book, self.book)

    # Test for viewing the cart contents.
    def test_view_cart_view(self):
        # Log in as the test user.
        self.client.login(username='testuser', password='testpass123')

        # Create a cart for the test user.
        cart = Cart.objects.create(user=self.user)

        # Create a cart item for the test book.
        CartItem.objects.create(cart=cart, book=self.book, quantity=1)

        # Simulate a GET request to the cart view.
        response = self.client.get(reverse('view_cart'))

        # Verify that the cart view loads successfully with a status code of 200.
        self.assertEqual(response.status_code, 200)

        # Confirm that the correct template is used for the cart view.
        self.assertTemplateUsed(response, 'store/cart.html')

        # Ensure that the 'cart' is passed to the template context.
        self.assertIn('cart', response.context)