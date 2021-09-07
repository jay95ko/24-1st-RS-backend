<<<<<<< HEAD
import json

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View

from carts.models import Cart
from users.models import User
from products.models import Product

class CartView(View):
    #@데코레이터
    def post(self, request):
        try:
            data       = json.loads(request.body)
            product_id = data['product_id']
            quantity   = data['quantity']
            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({"MESSAGE":"DOES_NOT_EXIST_ERROR"}, status=400)

            if Cart.objects.filter(id=product_id).exists():
                return JsonResponse({"MESSAGE":"ALREADY_EXIST"}, status=400)

            Cart.objects.create(
                user_id = 3             ,# 데코레이터에서 가져오기(토큰유저정보)
                product_id = product_id,
                quantity = quantity,
                )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

    def put(self, request):
        try:
            data = json.loads(request.body)
            count = data['count']
            cart = Cart.objects.get(id=id)
            if count == '+':
                cart.quantity += 1

            if count == '-' and cart.quantity > 1:
                cart.quantity -= 1

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

    def delete(request, product_id):
        cart = Cart.objects.get(product_id=25)
        cart.delete()
        # return redirect('url')
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

    #@데코레이터
    def get(self, request):
        result = list(Cart.objects.filter(user_id=3).values('user_id','product_id','quantity'))
        return JsonResponse({'RESULT':result}, status=200)
=======
>>>>>>> main
