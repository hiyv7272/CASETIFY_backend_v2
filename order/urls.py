from django.urls import path
from .views import (
    # CartView,
    CheckoutView,
    CheckoutDetailView
)
from .views import CartViewSet

urlpatterns = [
    # path('/cart', CartView.as_view()),
    path('/cart', CartViewSet.as_view({
        'post': 'insert_cart',
        'get': 'get_cart',
    })),
    path('/checkout', CheckoutView.as_view()),
    path('/checkout/detail', CheckoutDetailView.as_view()),
]
