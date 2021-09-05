import random

from django.core.exceptions import FieldError
from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from .models import Category, Description, Product, ProductFlavor, ProductImage, Brewery, Sidedish

def MakingList(queryset):
    products = queryset.select_related("category", "brewery").prefetch_related("images", "tag")
    result   = [{
                "id"               : product.id,
                "name"             : product.name,
                "price"            : format(product.price, ","),
                "dgree"            : product.dgree,
                "ml"               : product.ml,
                "awards"           : product.awards,
                "tiny_description" : product.tiny_description,
                "hash"             : [{"caption" : tag.caption} for tag in product.tag.all()],
                "grade"            : product.grade,
                "image"            : product.images.all()[0].image_url,
                "expire_date"      : product.expire_date,
                "keep"             : product.keep,
                "category_name"    : product.category.name,
            } for product in products]
    return result

class ImageListView(View):
    def get(self, request, product_id):
        try:
            result = [ProductImage.objects.filter(product_id = product_id).values("image_url")]
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
            result = [Sidedish.objects.filter(products = product_id).values("name", "image_url")]
            return JsonResponse({"Result": result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)

class DetailView(View):
    def get(self, request, product_id):
        try:
            result = [Description.objects.filter(product__id = product_id).values("point_flavor", "point_side", "point_story")]
            return JsonResponse({"Result": result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)

class ProductView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.filter(id=product_id)
            result  = MakingList(product)
            return JsonResponse({"Result": result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)

class ProductListView(View):
    def get(self, request):
        try:
            ORDER_BY   = request.GET.get("order-by", "id")
            OFFSET     = int(request.GET.get("offset", 0))
            LIMIT      = int(request.GET.get("limit", 2))
            CATEGORIES = request.GET.get("category")
            RANDOM     = bool(request.GET.get("random"))
            MIN_PRICE  = request.GET.get("min-price", 0)
            MAX_PRICE  = request.GET.get("max-price", 1000000)
            DEGREES    = request.GET.get("degree")
            products   = Product.objects.all().order_by(ORDER_BY)

            if CATEGORIES:
                query = Q()
                for CATEGORY in CATEGORIES.split(","):
                    query |= Q(category__name = CATEGORY)
                products = products.filter(query)

            if RANDOM:
                products_queryset  = []
                random_number_list = []
                for num in range(0,LIMIT):
                    random_number = random.randint(0,products.count()-1)

                    while random_number in random_number_list:
                        random_number = random.randint(0,products.count()-1)

                    random_number_list.append(random_number)
                    products_queryset.append(products[random_number])
                result = MakingList(products_queryset)
                return JsonResponse({"Result": result}, status=200)

            if DEGREES:
                query = Q()
                for DEGREE in DEGREES.split(","):
                    print(DEGREE)
                    query |= (Q(dgree__gte = int(DEGREE)-10) & Q(dgree__lte = int(DEGREE)))
                products = products.filter(query)

            query = Q(price__gte = MIN_PRICE) & Q(price__lte = MAX_PRICE)
            products = products.filter(query)

            products_queryset = products[OFFSET:OFFSET+LIMIT]

            result = MakingList(products_queryset)
            return JsonResponse({"Result": result}, status=200)

        except FieldError:
            return JsonResponse({"Result": "ORDER_BY_ERROR"}, status=400)

        except Category.DoesNotExist:
            return JsonResponse({"Result": "CATEGORY_DOES_NOT_EXIST"}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)

class CategoryView(View):
    def get(self, request, category):
        try:
            category = Category.objects.get(name__istartswith=category)

            if category.name == "약주" or category.name == "청주":
                result = {
                    "name"        : "약·청주",
                    "description" : category.description,
                    "image_url"   : category.image_url,
                }
                return JsonResponse({"Result": result}, status=200)
            
            result = {
                    "name"        : category.name,
                    "description" : category.description,
                    "image_url"   : category.image_url,
                }
            return JsonResponse({"Result": result}, status=200)

        except Category.DoesNotExist:
            return JsonResponse({"Result": "CATEGORY_DOES_NOT_EXIST"}, status=400)