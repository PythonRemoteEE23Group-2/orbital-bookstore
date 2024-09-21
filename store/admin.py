from django.contrib import admin
from .models import User, Category, Subcategory, Book, Review, Favorite, Cart, Order

# Register each model in the admin interface

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_admin', 'is_active')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'availability', 'category', 'subcategory')
    search_fields = ('title', 'author')
    list_filter = ('category', 'subcategory', 'availability')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'fav_rating')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'quantity', 'total_cost', 'created_at')
    list_filter = ('user',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'total_cost', 'status', 'payment_method', 'payment_status')
    list_filter = ('status', 'payment_method', 'payment_status')
