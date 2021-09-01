from django.urls import path

from .views import ProductsMainPageView

urlpatterns = [
    path("/main", ProductsMainPageView.as_view()),
]
