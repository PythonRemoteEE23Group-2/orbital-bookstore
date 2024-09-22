from django.shortcuts import render, redirect
from .models import Book, Category, Cart, Order, Favorite, Review
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import User
from django.shortcuts import get_object_or_404, redirect


def home(request):
    books = Book.objects.all()
    return render(request, 'store/home.html', {'books': books})


# Viewing a single book
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    reviews = Review.objects.filter(book=book)
    return render(request, 'store/book_detail.html', {'book': book, 'reviews': reviews})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # Redirect to the login page after registration
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})


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


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    if request.method == 'POST':
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                price=item.book.price,
                quantity=item.quantity,
                total_cost=item.total_cost,
                status='Pending',
                payment_method='Credit Card',  # Example hardcoded
                payment_status='Unpaid',
                delivery_email=request.user.email
            )
        cart_items.delete()  # Clear the user's cart after creating the order
        return redirect('order_success')  # Corrected URL redirection
    return render(request, 'store/checkout.html', {'cart_items': cart_items})


@login_required
def order_success(request):
    return render(request, 'store/order_success.html')


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

