import random
from django.core.exceptions import FieldError

from django.http import JsonResponse
from django.views import View
from django.db.models import Q, query

from .models import Category, Product, ProductFlavor, ProductImage, Brewery, Sidedish

def MakingList(queryset):
    res_list = []
    for product in queryset:

        hash_tag        = list(product.tag.all().values("caption"))
        first_image_url = product.images.all()[:1].get().image_url

        res_list.append(
            {
                "id"               : product.id,
                "name"             : product.name,
                "price"            : product.price,
                "dgree"            : product.dgree,
                "ml"               : product.ml,
                "awards"           : product.awards,
                "tiny_description" : product.tiny_description,
                "hash"             : hash_tag,
                "grade"            : product.grade,
                "image"            : first_image_url,
                "expire_date"      : product.expire_date,
                "keep"             : product.keep,
                "category_name"    : product.category.name,
            }
        )
    return res_list

class ImageListView(View):
    def get(self, request, product_id):
        try:
            images = list(ProductImage.objects.filter(product_id = product_id).values("image_url"))
            return JsonResponse({"Result": images}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)

class BreweryView(View):
    def get(self, request, product_id):
        try:
            breweries = []
            breweries.append(
                {
                    "brewery_name" : Brewery.objects.get(products = product_id).name,
                    "brewery_image": Brewery.objects.get(products = product_id).img_url,
                    }
                )
            return JsonResponse({"Result": breweries}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)

class FlavorListView(View):
    def get(self, request, product_id):
        try:
            products_flavors_queryset = ProductFlavor.objects.filter(product_id=product_id)
            flavors                   = []
            for product_flavor in products_flavors_queryset:
                flavors.append(
                    {
                        "flavor_name"      : product_flavor.flavor.flavor_name,
                        "point"            : product_flavor.point,
                    }
                )

            return JsonResponse({"Result": flavors}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)

class SidedishListView(View):
    def get(self, request, product_id):
        try:
            sidedishs = list(Sidedish.objects.filter(products = product_id).values("name", "image_url"))
            
            return JsonResponse({"Result": sidedishs}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)

class DetailView(View):
    def get(self, request, product_id):
        try:

            detailes = list(Product.objects.get(id=product_id).descriptions.all().values("point_flavor", "point_side", "point_story"))
            return JsonResponse({"Result": detailes}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)

class ProductView(View):
    def get(self, request, product_id):
        try:
            product      = Product.objects.filter(id=product_id)
            product_info = MakingList(product)
            return JsonResponse({"Result": product_info}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)