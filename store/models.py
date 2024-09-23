from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.TextField(blank=True, null=True)
    last_name = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    order_history = models.TextField(blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='store_user_groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='store_user_permissions',
        blank=True
    )


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cover_art = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    download_link = models.URLField(max_length=400)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)


class Favorite(models.Model):
    fav_rating = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50)
    delivery_email = models.CharField(max_length=255)
    email_sent_date = models.DateTimeField(null=True, blank=True)
    download_link = models.CharField(max_length=255, null=True, blank=True)
    download_expiry_date = models.DateTimeField(null=True, blank=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.book.title} - {self.order.user.username}'