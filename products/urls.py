from django.urls import path

from .views import CategoryView, CategoryListView, ProductView, DetailView, ImageListView, SidedishListView, FlavorListView, BreweryView, ProductListView

urlpatterns = [
    path("/<int:product_id>", ProductView.as_view()),
    path("/<int:product_id>/detail", DetailView.as_view()),
    path("/<int:product_id>/images", ImageListView.as_view()),
    path("/<int:product_id>/sidedishes", SidedishListView.as_view()),
    path("/<int:product_id>/flavors", FlavorListView.as_view()),
    path("/<int:product_id>/brewery", BreweryView.as_view()),
    path("/list", ProductListView.as_view()),
    path("/category/<int:category_id>", CategoryView.as_view()),
    path("/categories", CategoryListView.as_view()),
]