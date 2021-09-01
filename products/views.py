import random

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from .models import Product

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
        
        recommend_product_list = []
        for product_id in random_number_list:
            for category in category_product_list:
                
                first_image_url = category[product_id].images.all()[:1].get().image_url

                hash_tag = []
                for tag in category[product_id].tag.all():
                    hash_tag.append(tag.caption)

                recommend_product_list.append(
                    {
                        "id"               : category[product_id].id,
                        "name"             : category[product_id].name,
                        "tiny_description" : category[product_id].tiny_description,
                        "hash"             : hash_tag,
                        "grade"            : category[product_id].grade,
                        "image"            : first_image_url,
                    }
                )
        