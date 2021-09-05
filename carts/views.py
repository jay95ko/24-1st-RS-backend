import json

from django.http import JsonResponse
from django.views import View

from carts.models import Cart
from users.models import User
from products.models import Product

class CartView(View):
    # 데코레이터 필요
    def post(self, request):
        try:
            data       = json.loads(request.body)
            product_id = data['product_id']
            quantity   = data['quantity']
            if not Product.objects.get(id=product_id):
                return JsonResponse({"MESSAGE":"DOES_NOT_EXIST_ERROR"}, status=400)

            Cart.objects.create(
                user_id = 3             ,# 데코레이터에서 가져오기(토큰)
                product_id = product_id,
                quantity = quantity,
                )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

    # def put