import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.db.models import Q, Avg
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Category, Cart, CartItem, Order, Favorite, Review, User, PAYMENT_STATUS_CHOICES
from .forms import CustomUserCreationForm

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

    cart_items_count = 0
    user_has_reviewed = False

    if request.user.is_authenticated:
        cart_items_count = CartItem.objects.filter(cart__user=request.user).count()
        user_has_reviewed = reviews.filter(user=request.user).exists()

    context = {
        'book': book,
        'reviews': reviews,
        'user_has_reviewed': user_has_reviewed,
        'cart_items_count': cart_items_count,
    }

    return render(request, 'store/book_detail.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful registration
            messages.success(request, f'Account created for {user.username}!')
            return redirect('home')  # Redirect to the home page or dashboard
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
            return render(request, 'store/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'store/register.html', {'form': form})


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    CartItem.objects.create(cart=cart, book=book)

    messages.success(request, f'{book.title} has been added to your cart.')
    return redirect('view_cart')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        if action == 'add':
            cart_item.quantity += 1
        elif action == 'subtract':
            cart_item.quantity -= 1

        if cart_item.quantity > 0:
            cart_item.save()
        else:
            cart_item.delete()

        return redirect('view_cart')

    cart_items = cart.items.all()
    return render(
        request,
        'store/cart.html',
        {'cart': cart, 'cart_items': cart_items, 'cart_items_count': cart.items.count()}
    )


@login_required
def delete_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, f'{cart_item.book.title} has been removed from your cart.')
    return redirect('view_cart')


@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()
    total_cost = cart.total_cost

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        delivery_email = request.POST.get('email')

        if not payment_method:
            return render(request, 'store/checkout.html', {
                'cart_items': cart_items,
                'total_cost': total_cost,
                'cart_items_count': cart.items.count(),
                'error_message': 'Please select a payment method.'
            })

        # Create an order
        order = Order.objects.create(
            user=request.user,
            payment_method=payment_method,
            payment_status=PAYMENT_STATUS_CHOICES[0][0],
            delivery_email=delivery_email
        )

        # Link each CartItem to the order and mark as ordered
        for item in cart_items:
            item.ordered = True
            item.order = order
            item.save()

        # Clear cart by removing the ordered items

        # Confirm order placement
        messages.success(request, 'Your order has been placed successfully.')
        return redirect('order_success')

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'cart_items_count': cart.items.count(),
    })


@login_required
def order_success(request):
    latest_order = Order.objects.filter(user=request.user).order_by('-order_date').first()

    if latest_order:
        order_items = CartItem.objects.filter(order=latest_order)

    else:
        order_items = []

    Cart.objects.filter(user=request.user).delete()

    return render(request, 'store/order_success.html', {
        'order': latest_order,
        'order_items': order_items,
        'cart_items_count': 0,
    })


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
def delete_favorite(request, favorite_id):
    favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
    favorite.delete()
    return redirect('view_favorites')


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
    cart_item = CartItem.objects.filter(cart__user=request.user)
    return render(
        request,
        'store/favorites.html',
        {'favorites': favorites, 'cart_items_count': cart_item.count()}
    )


def view_reviews(request):
    reviews = Review.objects.all()

    if request.user.is_authenticated:
        cart_items_count = CartItem.objects.filter(cart__user=request.user).count()
    else:
        cart_items_count = None

    return render(
        request,
        'store/reviews.html',
        {'reviews': reviews, 'cart_items_count': cart_items_count}
    )



#get_cart_items_count()
