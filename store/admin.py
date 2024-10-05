from django.contrib import admin
from .models import User, Category, Subcategory, Book, Review, Favorite, Cart, CartItem, Order


# User Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_admin', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_admin', 'is_active')


# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


# Subcategory Admin
@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)


# Book Admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'availability', 'subcategory')
    search_fields = ('title', 'author')
    list_filter = ('subcategory__category', 'subcategory', 'availability')


# Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')


# Favorite Admin
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'book')


# Cart Admin
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'status', 'payment_method', 'payment_status', 'total_cost')
    list_filter = ('status', 'payment_method', 'payment_status')
    inlines = [CartItemInline]

    def total_cost(self, obj):
        return obj.total_cost
