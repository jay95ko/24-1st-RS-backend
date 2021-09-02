import random

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from .models import Product, ProductFlavor

def MakingList(queryset):
    list = []
    for product in queryset:

        hash_tag = []
        for tag in product.tag.all():
            hash_tag.append(tag.caption)

        first_image_url = product.images.all()[:1].get().image_url

        list.append(
            {
                "id"               : product.id,
                "name"             : product.name,
                "price"            : product.price,
                "tiny_description" : product.tiny_description,
                "hash"             : hash_tag,
                "grade"            : product.grade,
                "image"            : first_image_url,
            }
        )
    return list
class ProductsMainPageView(View):
    def get(self, request):
        
        fruit_wine = Product.objects.filter(category_id = 1)
        spirits    = Product.objects.filter(category_id = 2)
        takju      = Product.objects.filter(category_id = 4)
        rice_wine  = Product.objects.filter(Q(category_id = 5) | Q(category_id = 6))

        category_product_list = [fruit_wine, spirits, takju, rice_wine]
        
        random_number_list = []
        for num in range(0,2):
            random_number_list.append(random.randint(0,9))
        
        main_product_list      = []
        recommend_product_list = []
        sale_product_list      = []
        popular_product_list   = []
        new_product_list       = []
        recommend_objects      = []

        for product_id in random_number_list:
            for category in category_product_list:
                recommend_objects.append(category[product_id])
        recommend_product_list = MakingList(recommend_objects)
        
        sale_product         = Product.objects.get(id=15)
        sale_product_img_url = sale_product.images.all()[:1].get().image_url
        sale_product_list    = [
            {
                "id"               : sale_product.id,
                "name"             : sale_product.name,
                "price"            : sale_product.price,
                "image"            : sale_product_img_url,
            }
        ]
        
        popular_products     = Product.objects.all().order_by('-grade')[:3]
        popular_product_list = MakingList(popular_products)
        
        new_products     = Product.objects.all().order_by('-created_at')[:3]
        new_product_list = MakingList(new_products)

        main_product_list.append(
            {
                "recommend_product_list" : recommend_product_list,
                "sale_product_list"      : sale_product_list,
                "popular_product_list"   : popular_product_list,
                "new_product_list"       : new_product_list,
            }
        )

        return JsonResponse({"Result": main_product_list}, status=200)

class ProductsDetailPageView(View):
    def get(self, request, product_id):

        try:
            product = Product.objects.get(id=product_id)

            base_component           = []
            detail_component         = []
            description_component    = []
            sidedish_component       = []
            flavor_component         = []
            image_component          = []
            brewery_component        = []
            detail_product_component = []

            base_component = MakingList(Product.objects.filter(id=product_id))

            detail_component.append(
                {
                    "category_name" : product.category.name,
                    "dgree"         : product.dgree,
                    "ml"            : product.ml,
                    "expire_date"   : product.expire_date,
                    "keep"          : product.keep,
                }
            )

            description_component.append(
                {
                    "flavor" : product.descriptions.get().point_flavor,
                    "side"   : product.descriptions.get().point_side,
                    "story"  : product.descriptions.get().point_story,
                }
            )

            sidedishs = product.sidedish.all()
            for sidedish in sidedishs:
                sidedish_component.append(
                    {
                        "name"      : sidedish.name,
                        "image_url" : sidedish.image_url,
                    }
                )
            
            products_flavors = ProductFlavor.objects.filter(product=product)
            for product_flavor in products_flavors:
                flavor_component.append(
                    {
                        "flavor_name"      : product_flavor.flavor.flavor_name,
                        "point" : product_flavor.point,
                    }
                )
            
            images = product.images.all()
            for image in images:
                image_component.append(image.image_url)
            
            brewery_component.append(
                {
                    "brewery_name" : product.brewery.name,
                    "brewery_image": product.brewery.img_url,
                }
            )

            detail_product_component = [
                {
                    "base_component"        : base_component,
                    "detail_component"      : detail_component,
                    "description_component" : description_component,
                    "sidedish_component"    : sidedish_component,
                    "flavor_component"      : flavor_component,
                    "image_component"       : image_component,
                    "brewery_component"     : brewery_component,
                }
            ]
            return JsonResponse({"Result": detail_product_component}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({"Result": "PRODUCT_DOES_NOT_EXIST"}, status=400)