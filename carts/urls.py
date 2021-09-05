from django.urls import path
from carts.views import CartView

urlpatterns = [
    path('/cart', CartView.as_view()),
]