from .models import CartItem


def get_cart_items_count(user):
    if user.is_authenticated:
        return CartItem.objects.filter(cart__user=user).count()
    return 0

