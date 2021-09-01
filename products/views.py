import random

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from .models import Product

class ProductsMainPageView(View):
    def get(self, request):

        #rice_wine(약주, 청주)는 두가지의 주종을 포함하고 있음으로 Q객체 사용
        fruit_wine = Product.objects.filter(category_id = 1)
        spirits    = Product.objects.filter(category_id = 2)
        takju      = Product.objects.filter(category_id = 4)
        rice_wine  = Product.objects.filter(Q(category_id = 5) | Q(category_id = 6))

        #카테고리별 object를 담은 list
        category_product_list = [fruit_wine, spirits, takju, rice_wine]
        
        #주종별 2가지 주류를 추천하기 위한 난수 생성
        random_number_list = []
        for num in range(0,2):
            random_number_list.append(random.randint(0,9))
        
        #추천 주류를 담는 리스트 값 채우기
        recommend_product_list = []
        for product_id in random_number_list:
            #각 주종별 모든 object를 담은 list를 순회
            for category in category_product_list:
                
                #product_id는 위에서 생성된 난수가 들어가며 주종별 product_id는번째 주종의 object를 가져옴
                #category[product_id]로 랜덤한 object를 갖음
                #해당 M2M관계인 images 호출하여 첫번째 사진만 슬라이싱하여 받아옴
                #이때, queryset이 아닌 object로 받기 위해 get사요하여 원하는 image url받아오기
                first_image_url = category[product_id].images.all()[:1].get().image_url

                hash_tag = []
                for tag in category[product_id].tag.all():
                    hash_tag.append(tag.caption)

                recommend_product_list.append(
                    {
                        "id"               : category[product_id].id,
                        "name"             : category[product_id].name,
                        "price"            : category[product_id].price,
                        "tiny_description" : category[product_id].tiny_description,
                        "hash"             : hash_tag,
                        "grade"            : category[product_id].grade,
                        "image"            : first_image_url,
                    }
                )
        
        #세일하는 주류
        sale_product         = Product.objects.get(id=15)
        sale_product_img_url = sale_product.images.all()[:1].get().image_url
        sale_product = [
            {
                "id"               : sale_product.id,
                "name"             : sale_product.name,
                "price"            : sale_product.price,
                "image"            : sale_product_img_url,
            }
        ]

        #인기제품 3가지 list
        popular_product_list = []
        popular_products = Product.objects.all().order_by('-grade')[:3]
        for product in popular_products:

            hash_tag = []
            for tag in product.tag.all():
                hash_tag.append(tag.caption)

            first_image_url = product.images.all()[:1].get().image_url

            popular_product_list.append(
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

        #신상품 3가지 list
        new_product_list = []
        new_products = Product.objects.all().order_by('-created_at')[:3]
        for product in new_products:

            hash_tag = []
            for tag in product.tag.all():
                hash_tag.append(tag.caption)

            first_image_url = product.images.all()[:1].get().image_url

            new_product_list.append(
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