import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import Q, Avg, Sum, F
from .models import Book, Category, Cart, CartItem, Order, OrderItem, Favorite, Review, User

logger = logging.getLogger(__name__)


def home(request):
    query = request.GET.get('q')
    selected_category = request.GET.get('category')

    books = Book.objects.all()

    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))

    if selected_category:
        books = books.filter(subcategory__category__id=selected_category)

    categories = Category.objects.prefetch_related('subcategories__books')

    cart_items_count = CartItem.objects.filter(cart__user=request.user).count() if request.user.is_authenticated else 0

    books = books.annotate(average_rating=Avg('reviews__rating'))

    return render(request, 'store/home.html', {
        'categories': categories,
        'books': books,
        'cart_items_count': cart_items_count,
        'selected_category': selected_category,
        'query': query,
    })


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.all()
    return render(request, 'store/book_detail.html', {'book': book, 'reviews': reviews})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'store/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'store/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'store/register.html')

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password1)
        )

        login(request, user)

        messages.success(request, f'Account created for {user.username}!')
        return redirect('home')

    return render(request, 'store/register.html')


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f'{book.title} has been added to your cart.')
    return redirect('view_cart')


@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_cost = cart.total_cost
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_cost': total_cost})


@login_required
def delete_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, f'{cart_item.book.title} has been removed from your cart.')
    return redirect('view_cart')


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_cost = cart.total_cost

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        delivery_email = request.POST.get('email')

        if not payment_method:
            return render(request, 'store/checkout.html', {
                'cart_items': cart_items,
                'total_cost': total_cost,
                'error_message': 'Please select a payment method.'
            })

        order = Order.objects.create(
            user=request.user,
            payment_method=payment_method,
            payment_status='pending',
            delivery_email=delivery_email
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )

        cart.items.all().delete()
        messages.success(request, 'Your order has been placed successfully.')
        return redirect('order_success')

    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'total_cost': total_cost})


@login_required
def order_success(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')[:5]
    return render(request, 'store/order_success.html', {'orders': orders})


@login_required
def add_to_favorites(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)

    if created:
        messages.success(request, f'{book.title} has been added to your favorites.')
    else:
        messages.info(request, f'{book.title} is already in your favorites.')

    return redirect('book_detail', book_id=book_id)


@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')

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
