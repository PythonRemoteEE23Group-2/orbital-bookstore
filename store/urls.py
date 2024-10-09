from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import home, toggle_favorites

urlpatterns = [
    path('', views.home, name='home'),
    path('', home, name='home'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('delete-from-cart/<int:cart_item_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='store/logout.html'), name='logout'),
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('favorites/delete/<int:favorite_id>/', views.delete_favorite, name='delete_favorite'),
    path('add-to-favorites/<int:book_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('reviews/', views.view_reviews, name='view_reviews'),
    path('add-review/<int:book_id>/', views.add_review, name='add_review'),
    path('book/<int:book_id>/toggle-favorites/', views.toggle_favorites, name='toggle_favorites'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('toggle_favorites/<int:book_id>/', toggle_favorites, name='toggle_favorites'),
]