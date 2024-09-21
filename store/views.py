from django.shortcuts import render, redirect
from .models import Book, Category, Cart, Order, Favorite, Review
from django.contrib.auth.decorators import login_required


# Homepage: showing all books
def home(request):
    books = Book.objects.all()
    return render(request, 'store/home.html', {'books': books})


# Viewing a single book
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    reviews = Review.objects.filter(book=book)
    return render(request, 'store/book_detail.html', {'book': book, 'reviews': reviews})


# Adding a book to the cart
@login_required
def add_to_cart(request, book_id):
    book = Book.objects.get(id=book_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
    cart_item.quantity += 1
    cart_item.total_cost = cart_item.quantity * cart_item.book.price
    cart_item.save()
    return redirect('view_cart')


# Viewing the cart
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})


# Checkout process
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
        cart_items.delete()
        return redirect('order_success')
    return render(request, 'checkout.html', {'cart_items': cart_items})


# Success page after placing an order
@login_required
def order_success(request):
    return render(request, 'order_success.html')
