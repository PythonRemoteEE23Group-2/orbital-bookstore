import logging
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import Book, Ebook, Accessory, BookWrap, Exlibris, SchoolOffice, BookletFolder, Pencil, Other, Cart, Order, Favorite, Review




def home(request):
    cart_items_count = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    return render(request, 'store/home.html', {'cart_items_count': cart_items_count})


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
def add_to_cart(request, item_id):
    # Fetch each item type and only add the one that is found
    book = Book.objects.filter(id=item_id).first()
    ebook = Ebook.objects.filter(id=item_id).first()
    accessory = Accessory.objects.filter(id=item_id).first()
    pencil = Pencil.objects.filter(id=item_id).first()
    other = Other.objects.filter(id=item_id).first()
    book_wrap = BookWrap.objects.filter(id=item_id).first()
    exlibris = Exlibris.objects.filter(id=item_id).first()
    booklet_folder = BookletFolder.objects.filter(id=item_id).first()
    school_office = SchoolOffice.objects.filter(id=item_id).first()

    cart_item = None

    if book:
        cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
    elif ebook:
        cart_item, created = Cart.objects.get_or_create(user=request.user, ebook=ebook)
    elif accessory:
        cart_item, created = Cart.objects.get_or_create(user=request.user, accessory=accessory)
    elif school_office:
        cart_item, created = Cart.objects.get_or_create(user=request.user, school_office=school_office)
    elif pencil:
        cart_item, created = Cart.objects.get_or_create(user=request.user, pencil=pencil)
    elif other:
        cart_item, created = Cart.objects.get_or_create(user=request.user, other=other)
    elif book_wrap:
        cart_item, created = Cart.objects.get_or_create(user=request.user, book_wrap=book_wrap)
    elif exlibris:
        cart_item, created = Cart.objects.get_or_create(user=request.user, exlibris=exlibris)
    elif booklet_folder:
        cart_item, created = Cart.objects.get_or_create(user=request.user, booklet_folder=booklet_folder)
    else:
        messages.error(request, "Item not found.")
        return redirect('home')

    # Update quantity and total cost
    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1

    # Set the correct price based on the item type
    if book:
        cart_item.total_cost = cart_item.quantity * book.price
    elif ebook:
        cart_item.total_cost = cart_item.quantity * ebook.price
    elif accessory:
        cart_item.total_cost = cart_item.quantity * accessory.price
    elif school_office:
        cart_item.total_cost = cart_item.quantity * school_office.price
    elif pencil:
        cart_item.total_cost = cart_item.quantity * pencil.price
    elif other:
        cart_item.total_cost = cart_item.quantity * other.price
    elif book_wrap:
        cart_item.total_cost = cart_item.quantity * book_wrap.price
    elif exlibris:
        cart_item.total_cost = cart_item.quantity * exlibris.price
    elif booklet_folder:
        cart_item.total_cost = cart_item.quantity * booklet_folder.price

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

    # Update total price calculation to check all item types
    total_price = sum(
        (item.book.price if item.book else 0) +
        (item.ebook.price if item.ebook else 0) +
        (item.accessory.price if item.accessory else 0) +
        (item.pencil.price if item.pencil else 0) +
        (item.other.price if item.other else 0) +
        (item.book_wrap.price if item.book_wrap else 0) +
        (item.exlibris.price if item.exlibris else 0) +
        (item.booklet_folder.price if item.booklet_folder else 0) +
        (item.school_office.price if item.school_office else 0)
        for item in cart_items
    )

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        delivery_email = request.POST.get('email')

        if not payment_method:
            return render(request, 'store/checkout.html', {
                'cart_items': cart_items,
                'total_price': total_price,
                'error_message': 'Please select a payment method.'
            })

        for item in cart_items:
            order_data = {
                'user': request.user,
                'price': item.total_cost / item.quantity,  # Use per-item price
                'quantity': item.quantity,
                'total_cost': item.total_cost,
                'status': 'Pending',
                'payment_method': payment_method,
                'payment_status': 'Unpaid',
                'delivery_email': delivery_email,
            }

            # Create an Order for the correct item type
            if item.book:
                order_data['book'] = item.book
            elif item.ebook:
                order_data['ebook'] = item.ebook
            elif item.accessory:
                order_data['accessory'] = item.accessory
            elif item.pencil:
                order_data['pencil'] = item.pencil
            elif item.other:
                order_data['other'] = item.other
            elif item.book_wrap:
                order_data['book_wrap'] = item.book_wrap
            elif item.exlibris:
                order_data['exlibris'] = item.exlibris
            elif item.booklet_folder:
                order_data['booklet_folder'] = item.booklet_folder
            elif item.school_office:
                order_data['school_office'] = item.school_office

            # Create the Order
            Order.objects.create(**order_data)

        cart_items.delete()  # Clear the cart after order creation
        return redirect('order_success')

    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def order_success(request):
    # Fetch recent orders using order_date
    orders = Order.objects.filter(user=request.user).order_by('-order_date')[:5]
    return render(request, 'store/order_success.html', {'orders': orders})


@login_required
def add_to_favorites(request, item_id):
    # Fetch items from all possible models
    book = Book.objects.filter(id=item_id).first()
    ebook = Ebook.objects.filter(id=item_id).first()
    accessory = Accessory.objects.filter(id=item_id).first()

    # Check and add the item to favorites
    if book:
        favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)
    elif ebook:
        favorite, created = Favorite.objects.get_or_create(user=request.user, ebook=ebook)
    elif accessory:
        favorite, created = Favorite.objects.get_or_create(user=request.user, accessory=accessory)
    else:
        messages.error(request, "Item not found.")
        return redirect('home')

    if created:
        messages.success(request, 'Item added to your favorites.')
    else:
        messages.info(request, 'Item is already in your favorites.')

    return redirect('home')


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

    # Handle the quantity increase/decrease
    if operation == 'increase':
        cart_item.quantity += 1
    elif operation == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    elif operation == 'decrease' and cart_item.quantity == 1:
        # If quantity reaches 0, remove the item
        cart_item.delete()
        return redirect('view_cart')

    # Update the total cost based on the item type
    if cart_item.book:
        cart_item.total_cost = cart_item.quantity * cart_item.book.price
    elif cart_item.ebook:
        cart_item.total_cost = cart_item.quantity * cart_item.ebook.price
    elif cart_item.accessory:
        cart_item.total_cost = cart_item.quantity * cart_item.accessory.price
    elif cart_item.pencil:
        cart_item.total_cost = cart_item.quantity * cart_item.pencil.price
    elif cart_item.other:
        cart_item.total_cost = cart_item.quantity * cart_item.other.price
    elif cart_item.book_wrap:
        cart_item.total_cost = cart_item.quantity * cart_item.book_wrap.price
    elif cart_item.exlibris:
        cart_item.total_cost = cart_item.quantity * cart_item.exlibris.price
    elif cart_item.booklet_folder:
        cart_item.total_cost = cart_item.quantity * cart_item.booklet_folder.price
    elif cart_item.school_office:
        cart_item.total_cost = cart_item.quantity * cart_item.school_office.price
    else:
        cart_item.total_cost = 0  # Set a default value or handle the error

    cart_item.save()
    return redirect('view_cart')


def search(request):
    query = request.GET.get('q', '')

    if query:
        # Fetching books, ebooks, and other items based on query
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )
        ebooks = Ebook.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )
        accessories = Accessory.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
        book_wraps = BookWrap.objects.filter(
            Q(accessory__name__icontains=query) |
            Q(color__icontains=query)
        )
        booklets_folders = BookletFolder.objects.filter(
            Q(school_office__name__icontains=query) |
            Q(size__icontains=query)
        )
        exlibris = Exlibris.objects.filter(
            Q(accessory__name__icontains=query) |
            Q(design__icontains=query)
        )
        pencils = Pencil.objects.filter(
            Q(school_office__name__icontains=query) |
            Q(pencil_type__icontains=query)
        )
        school_and_office = SchoolOffice.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

        # Combine results from all item types into one list
        items = list(books) + list(ebooks) + list(accessories) + list(book_wraps) + \
                list(school_and_office) + list(exlibris) + list(pencils) + list(booklets_folders)
    else:
        items = []

    return render(request, 'store/search_results.html', {'items': items})


def about_us(request):
    return render(request, 'store/about_us.html')


def contact_us(request):
    return render(request, 'store/contact_us.html')


def terms_and_conditions(request):
    return render(request, 'store/terms_and_conditions.html')


def shipping_information(request):
    return render(request, 'store/shipping_information.html')


def books(request):
    return render(request, 'store/books.html')


def ebooks(request):
    return render(request, 'store/ebooks.html')


def accessories(request):
    return render(request, 'store/accessories.html')


def book_wraps(request):
    book_wraps = BookWrap.objects.all()  # Fetch all book wraps
    return render(request, 'store/book_wraps.html', {'book_wraps': book_wraps})


def exlibris(request):
    exlibris_items = Exlibris.objects.all()  # Fetch all exlibris
    return render(request, 'store/exlibris.html', {'exlibris_items': exlibris_items})


def school_and_office(request):
    return render(request, 'store/school_and_office.html')


def booklets_folders(request):
    booklets_folders = BookletFolder.objects.all()  # Fetch all booklets/folders
    return render(request, 'store/booklets_folders.html', {'booklets_folders': booklets_folders})


def pencils(request):
    pencils = Pencil.objects.all()  # Fetch all pencils
    return render(request, 'store/pencils.html', {'pencils': pencils})



def other(request):
    return render(request, 'store/other.html')


def books_view(request):
    books = Book.objects.all()  # Fetch all books from the database
    return render(request, 'store/books.html', {'books': books})


# View for E-books page
def ebooks_view(request):
    ebooks = Ebook.objects.all()  # Fetch all e-books
    return render(request, 'store/ebooks.html', {'ebooks': ebooks})


def ebook_detail(request, ebook_id):
    ebook = get_object_or_404(Ebook, id=ebook_id)  # Fetch the e-book or return a 404 error
    return render(request, 'store/e-book_details.html', {'ebook': ebook})
