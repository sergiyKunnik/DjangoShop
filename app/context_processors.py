from .views import get_cart
from .models import Category


def cart_categories(request):
    cart = get_cart(request)
    return {
        'cart': cart,
        'categories': Category.objects.all()
    }