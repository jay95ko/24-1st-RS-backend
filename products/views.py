import random

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from .models import Product

class ProductsMainPageView(View):
    def get(self, request):

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
        
        #rice_wine(약주, 청주)는 두가지의 주종을 포함하고 있음으로 Q객체 사용
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