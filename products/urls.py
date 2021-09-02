from django.urls import path

from .views import ProductsMainPageView, ProductsDetailPageView

urlpatterns = [
    path("/main", ProductsMainPageView.as_view()),
    path("/detail/<int:product_id>", ProductsDetailPageView.as_view()),
]
