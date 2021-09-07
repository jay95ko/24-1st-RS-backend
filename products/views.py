import random

from django.core.exceptions import FieldError
from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from .models import Category, Product

def make_list(queryset):
    products = queryset.select_related("category", "brewery").prefetch_related("images", "tag", "sidedish")
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
                "side_dish"        : [{"name" : sidedish.name, "image_url" : sidedish.image_url} for sidedish in product.sidedish.all()],
            } for product in products]
    return result

class ProductView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.filter(id=product_id)
            result  = make_list(product)
            return JsonResponse({"Result": result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)

class ProductListView(View):
    def get(self, request):
        try:
            ORDER_BY   = request.GET.get("order-by", "id")
            OFFSET     = int(request.GET.get("offset", 0))
            LIMIT      = int(request.GET.get("limit", 10))
            CATEGORIES = request.GET.get("category")
            RANDOM     = bool(request.GET.get("random"))
            MIN_PRICE  = request.GET.get("min-price", 0)
            MAX_PRICE  = request.GET.get("max-price", 1000000)
            DEGREES    = request.GET.get("degree")
            SIDEDISH   = request.GET.get("side-dish")
            products   = Product.objects.all().order_by(ORDER_BY)

            if CATEGORIES:
                query = Q()
                [query.add(Q(category__name = CATEGORY), query.OR) for CATEGORY in CATEGORIES.split(",")]
                products = products.filter(query)

            if RANDOM:
                products_queryset = products.order_by("?")[:LIMIT]
                result = make_list(products_queryset)
                return JsonResponse({"Result": result}, status=200)

            if DEGREES:
                query = Q()
                [query.add(Q(dgree__gte = int(DEGREE)-10) & Q(dgree__lte = int(DEGREE)), query.OR) for DEGREE in DEGREES.split(",")]
                products = products.filter(query)
            
            if SIDEDISH:
                products = products.filter(sidedish__name__contains = SIDEDISH)
                
            query = Q(price__gte = MIN_PRICE) & Q(price__lte = MAX_PRICE)
            products = products.filter(query)

            products_queryset = products[OFFSET:OFFSET+LIMIT]

            result = make_list(products_queryset)
            return JsonResponse({"Result": result}, status=200)

        except FieldError:
            return JsonResponse({"Result": "ORDER_BY_ERROR"}, status=400)

        except Category.DoesNotExist:
            return JsonResponse({"Result": "CATEGORY_DOES_NOT_EXIST"}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)
