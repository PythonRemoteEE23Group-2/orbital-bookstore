import logging
from django.db.models import Q
from django.shortcuts import render
from .models import Book, Category, Cart, Order, Favorite, Review, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from django.shortcuts import get_object_or_404, redirect
from django import forms
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


def home(request):
    books = Book.objects.all()
    cart_items_count = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    return render(request, 'store/home.html', {'books': books, 'cart_items_count': cart_items_count})


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    reviews = Review.objects.filter(book=book)
    return render(request, 'store/book_detail.html', {'book': book, 'reviews': reviews})


User = get_user_model()


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Basic validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'store/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'store/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'store/register.html')

        # Create the user
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password1)  # Hash the password manually
        )

        # Log the user in after registration (optional)
        login(request, user)

        messages.success(request, f'Account created for {user.username}!')
        return redirect('home')  # Redirect after successful registration

    return render(request, 'store/register.html')


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)

    if created:
        cart_item.quantity = 1
        cart_item.total_cost = book.price
    else:
        cart_item.quantity += 1
        cart_item.total_cost = cart_item.quantity * book.price

    cart_item.save()
    return redirect('view_cart')


# Viewing the cart
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'store/cart.html', {'cart_items': cart_items})


logger = logging.getLogger(__name__)


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')  # Redirect to the cart page after deletion


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.book.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        # Get the payment method from the form
        payment_method = request.POST.get('payment_method')
        delivery_email = request.POST.get('email')

        # Check if payment method is provided
        if not payment_method:
            return render(request, 'store/checkout.html', {
                'cart_items': cart_items,
                'total_price': total_price,
                'error_message': 'Please select a payment method.'
            })

        # Create the orders
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                book=item.book,
                price=item.book.price,
                quantity=item.quantity,
                total_cost=item.book.price * item.quantity,
                status='Pending',
                payment_method=payment_method,  # Pass the payment method here
                payment_status='Unpaid',
                delivery_email=delivery_email
            )

        cart_items.delete()  # Clear the cart after order is created
        return redirect('order_success')

    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def order_success(request):
    # Fetch recent orders using order_date
    orders = Order.objects.filter(user=request.user).order_by('-order_date')[:5]
    return render(request, 'store/order_success.html', {'orders': orders})


@login_required
def add_to_favorites(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'fav_rating': 1}
    )

    if created:
        messages.success(request, f'{book.title} has been added to your favorites.')
    else:
        messages.info(request, f'{book.title} is already in your favorites.')

    return redirect('book_detail', book_id=book_id)


@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        rating = request.POST['rating']
        review_text = request.POST['review_text']

        Review.objects.create(
            user=request.user,
            book=book,
            rating=rating,
            review_text=review_text
        )
        messages.success(request, 'Your review has been added.')
        return redirect('book_detail', book_id=book_id)

    return render(request, 'store/add_review.html', {'book': book})


@login_required
def view_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'store/favorites.html', {'favorites': favorites})


@login_required
def view_reviews(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'store/reviews.html', {'reviews': reviews})


@login_required
def update_cart_quantity(request, item_id, operation):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)

    if operation == 'increase':
        cart_item.quantity += 1
    elif operation == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    elif operation == 'decrease' and cart_item.quantity == 1:
        # If quantity reaches 0, remove the item
        cart_item.delete()
        return redirect('view_cart')

    cart_item.total_cost = cart_item.quantity * cart_item.book.price
    cart_item.save()

    return redirect('view_cart')


def search(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        books = Book.objects.none()

    return render(request, 'store/search_results.html', {'books': books})

def about_us(request):
    return render(request, 'store/about_us.html')

def contact_us(request):
    return render(request, 'store/contact_us.html')

def terms_and_conditions(request):
    return render(request, 'store/terms_and_conditions.html')

def shipping_information(request):
    return render(request, 'store/shipping_information.html')
