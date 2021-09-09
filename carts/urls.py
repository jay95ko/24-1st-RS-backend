from django.urls import path
from carts.views import CartView, CartEditView

urlpatterns = [
    path('', CartView.as_view()),
    path('/<int:cart_id>', CartEditView.as_view()),
]