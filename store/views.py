from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    books = Book.objects.all()


def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    reviews = Review.objects.filter(book=book)
    return render(request, 'store/book_detail.html', {'book': book, 'reviews': reviews})


def register(request):
    if request.method == 'POST':


@login_required
def add_to_cart(request, book_id):
    cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')


# Viewing the cart
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    if request.method == 'POST':
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                price=item.book.price,
                quantity=item.quantity,
                status='Pending',
                payment_status='Unpaid',
            )
        return redirect('order_success')


@login_required
def order_success(request):
