from django.http import JsonResponse
from django.views import View

from .models import Description, Product, ProductFlavor, ProductImage, Brewery, Sidedish

class ImageListView(View):
    def get(self, request, product_id):
        try:
            result = list(ProductImage.objects.filter(product_id = product_id).values("image_url"))
            return JsonResponse({"Result": result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)

class BreweryView(View):
    def get(self, request, product_id):
        try:
            brewery = Brewery.objects.get(products__id = product_id)
            result  = {"brewery_name" : brewery.name, "brewery_image": brewery.img_url}
            return JsonResponse({"Result": result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)

class FlavorListView(View):
    def get(self, request, product_id):
        try:
            flavors = ProductFlavor.objects.select_related("flavor").filter(product_id=product_id)
            result  = [{"flavor_name" : flavor.flavor.flavor_name, "point" : flavor.point} for flavor in flavors]
            return JsonResponse({"Result": result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)

class SidedishListView(View):
    def get(self, request, product_id):
        try:
            result = list(Sidedish.objects.filter(products = product_id).values("name", "image_url"))
            return JsonResponse({"Result": result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)

class DetailView(View):
    def get(self, request, product_id):
        try:
            result = list(Description.objects.filter(product__id = product_id).values("point_flavor", "point_side", "point_story"))
            return JsonResponse({"Result": result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)