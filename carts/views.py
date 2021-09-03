
from django.db import models
from django.http import JsonResponse
from django.views import View

from carts.models import Cart 
from users.models import User
from products.models import Product

class CartsView(View):
    # def get(self, request):
        # users = User.objects.all()
        # result = []
        # for user in users:
        #     product_list = []
        #     products = Product.objects.all()
        #     for product in products:
        #         product_list.append(
        #             {
        #                 "product": product.name
        #             }
        #         )
        #     result.append(
        #         {
        #             "user": user.name, #email
        #             "product": product_list,
        #         }
        #     )
        #     return JsonResponse({'result':result}, status=200)

    def get(self, request):
        user = User.objects.get(email = email)
        cart = Cart.objects.get(user=user)
        cart.product



        quantity


