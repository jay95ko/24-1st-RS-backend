from django.urls import path

from .views import ProductView, DetailView, ImageListView, SidedishListView, BreweryView, FlavorListView, ProductListView, CategoryView

urlpatterns = [
    path("/<int:product_id>", ProductView.as_view()),
    path("/<int:product_id>/detail", DetailView.as_view()),
    path("/<int:product_id>/images", ImageListView.as_view()),
    path("/<int:product_id>/sidedishes", SidedishListView.as_view()),
    path("/<int:product_id>/flavors", FlavorListView.as_view()),
    path("/<int:product_id>/brewery", BreweryView.as_view()),
    path("/list", ProductListView.as_view()),
    path("/category/<category>", CategoryView.as_view()),
]
