import json

from django.http import JsonResponse
from django.views import View

from carts.models import Cart
from users.models import User
from products.models import Product

class CartView(View):
    #@데코레이터
    def post(self, request):
            data       = json.loads(request.body)
            product_id = data['product_id']
            quantity   = data['quantity']
           
            try:
                if not Product.objects.filter(id=product_id).exists():
                    return JsonResponse({"MESSAGE":"DOES_NOT_EXIST_ERROR"}, status=400)

                Cart.objects.create(
                    user_id = 3             ,# 데코레이터에서 가져오기(토큰유저정보)
                    product_id = product_id,
                    quantity = quantity,
                    )
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

            except KeyError:
                return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

    # def put(self, request):
    #         data = json.loads(request.body)
    #         count = data['count']
    #         delete = data['delete']
    #         cart = Cart.objects.get(id=id)
        
    #         try:
    #             if count == '+' and cart.quantity > 0:
    #                 cart.quantity += 1

    #             if count == '-' and cart.quantity > 1:
    #                 cart.quantity -= 1

    #             if delete:
    #                 cart.delete()
    #                 return JsonResponse({'MESSAGE':'DELETE'}, status=201)

    #             return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

    #         except KeyError:
    #             return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

    #@데코레이터
    def get(self, request):
        # carts = Cart.objects.filter(user_id=3).values()
        print('aa')
        result = list(Cart.objects.filter(user_id=3).values('user_id','product_id','quantity'))
        # for cart in carts:
        #     result.append(
        #         {
        #             'user': cart.user_id,
        #             'product': cart.product_id,
        #             'quantity': cart.quantity,
        #         }
        #     )
        return JsonResponse({'RESULT':result}, status=200)
