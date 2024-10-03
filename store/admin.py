from django.contrib import admin
from .models import User, Category, Subcategory, Book, Review, Favorite, Cart, CartItem, Order, OrderItem


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
    list_display = ('title', 'author', 'price', 'availability', 'subcategory')
    search_fields = ('title', 'author')
    list_filter = ('subcategory__category', 'subcategory', 'availability')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'book')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'total_cost')
    inlines = [CartItemInline]

    def total_cost(self, obj):
        return obj.total_cost

    total_cost.short_description = 'Total Cost'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'status', 'payment_method', 'payment_status', 'total_cost')
    list_filter = ('status', 'payment_method', 'payment_status')
    inlines = [OrderItemInline]

    def total_cost(self, obj):
        return obj.total_cost

    total_cost.short_description = 'Total Cost'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'book', 'quantity', 'subtotal')
    list_filter = ('cart__user',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity', 'price', 'subtotal')
    list_filter = ('order__user',)
