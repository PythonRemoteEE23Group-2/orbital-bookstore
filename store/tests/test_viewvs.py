from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from store.models import Book, Category, Subcategory, Cart, CartItem, Review

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test Category')
        self.subcategory = Subcategory.objects.create(name='Test Subcategory', category=self.category)
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            price=9.99,
            subcategory=self.subcategory
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/home.html')
        self.assertIn('books', response.context)
        self.assertIn('categories', response.context)

    def test_book_detail_view(self):
        response = self.client.get(reverse('book_detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/book_detail.html')
        self.assertEqual(response.context['book'], self.book)

    def test_add_to_cart_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('add_to_cart', args=[self.book.id]))
        self.assertRedirects(response, reverse('view_cart'))
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(cart.items.first().book, self.book)

    def test_view_cart_view(self):
        self.client.login(username='testuser', password='testpass123')
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, book=self.book)
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/cart.html')
        self.assertEqual(response.context['cart'], cart)

    def test_add_review_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('add_review', args=[self.book.id]), {
            'rating': 5,
            'review': 'Great book!'
        })
        self.assertRedirects(response, reverse('book_detail', args=[self.book.id]))
        self.assertEqual(Review.objects.count(), 1)
        review = Review.objects.first()
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.book, self.book)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.review_text, 'Great book!')