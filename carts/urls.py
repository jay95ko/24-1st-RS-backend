from django.urls import path
from carts.views import CartView

urlpatterns = [
    path('', CartView.as_view()),
    # path('/cart/<int:product_id>', CartView.as_view)
]