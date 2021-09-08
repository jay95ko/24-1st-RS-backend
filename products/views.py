import json

from django.core.exceptions import FieldError
from django.http import JsonResponse
from django.views import View
from django.db.models import Q, Sum

from .models import Product, Description, ProductFlavor, ProductImage, Brewery, Sidedish, Category, OrderItem, Order
from users.decorator import login_decorator

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

class CategoryView(View):
    def get(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
            result = {
                    "name"        : category.name,
                    "description" : category.description,
                    "image_url"   : category.image_url,
                }
            return JsonResponse({"Result": result}, status=200)

        except Category.DoesNotExist:
            return JsonResponse({"Result": "CATEGORY_DOES_NOT_EXIST"}, status=404)

class CategoryListView(View):
    def get(self, request):
        try:
            categories = Category.objects.all()
            result = [{
                    "id"          : category.id,
                    "name"        : category.name,
                    "description" : category.description,
                    "image_url"   : category.image_url,
                } for category in categories]
            return JsonResponse({"Result": result}, status=200)

        except Category.DoesNotExist:
            return JsonResponse({"Result": "CATEGORY_DOES_NOT_EXIST"}, status=404)

class OrderView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            ADDRESS      = data["address"]
            PHONE_NUMBER = data["phone_number"]
            order_item  = data["order_items"]

            order_product_list = [item["product_id"] for item in order_item]

            order_products = Product.objects.filter(id__in = order_product_list)

            order = Order.objects.create(
                user         = request.user,
                address      = ADDRESS,
                phone_number = PHONE_NUMBER
            )

            order_item_list = [OrderItem(
                    product_id = item["product_id"],
                    order      = order,
                    quantity   = item["quantity"],
                    price      = (order_products.get(id = item["product_id"]).price * item["quantity"])
                ) for item in order_item]

            OrderItem.objects.bulk_create(order_item_list)

            order.price = order.order_items.all().aggregate(Sum("price"))["price__sum"]
            order.save()

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)