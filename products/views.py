from django.core.exceptions import FieldError
from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from .models import Product

class ProductView(View):
    def get(self, request, product_id):
        try:
            product = Product.objects.filter(id=product_id).select_related("category", "brewery").prefetch_related("images", "tag", "sidedish").get()
            result  = {
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
            }
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
            MIN_PRICE  = request.GET.get("min-price", 0)
            MAX_PRICE  = request.GET.get("max-price", 1000000)
            DEGREES    = request.GET.get("degree")
            SIDEDISH   = request.GET.get("side-dish")
            products   = Product.objects.all().order_by(ORDER_BY)

            if CATEGORIES:
                products = products.filter(category__id__in=CATEGORIES.split(","))

            if DEGREES:
                query = Q()
                [query.add(Q(dgree__gte = int(DEGREE)-10) & Q(dgree__lte = int(DEGREE)), query.OR) for DEGREE in DEGREES.split(",")]
                products = products.filter(query)
            
            if SIDEDISH:
                products = products.filter(sidedish__name__contains = SIDEDISH)
                
            query = Q(price__gte = MIN_PRICE) & Q(price__lte = MAX_PRICE)
            products = products.filter(query)

            products_queryset = products[OFFSET:OFFSET+LIMIT]

            products = products_queryset.select_related("category", "brewery").prefetch_related("images", "tag", "sidedish")
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
            return JsonResponse({"Result": result}, status=200)

        except FieldError:
            return JsonResponse({"Result": "ORDER_BY_ERROR"}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)