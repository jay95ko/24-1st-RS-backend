import json

from django.http import JsonResponse
from django.views import View

from carts.models import Cart
from products.models import Product
from users.decorator import login_decorator

class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            product_id = data['product_id']
            quantity   = data['quantity']

            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({"MESSAGE":"DOES_NOT_EXIST_ERROR"}, status=400)

            if Cart.objects.filter(product_id=product_id).exists():
                return JsonResponse({"MESSAGE":"ALREADY_EXIST"}, status=400)

            Cart.objects.create(
                user       = request.user,
                product_id = product_id,
                quantity   = quantity,
                )

            return JsonResponse({'MESSAGE':'CREATE'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

    @login_decorator
    def get(self, request):
        carts = Cart.objects.select_related("product","product__brewery").filter(user_id=request.user).prefetch_related("product__images")
        Result = [{
            "cart_id"       : cart.id,
            "user_name"     : request.user.name,
            "product_id"    : cart.product.id, 
            "product_name"  : cart.product.name, 
            "quantity"      : cart.quantity,
            "product_price" : cart.product.price, 
            "image_url"     : cart.product.images.first().image_url
            }for cart in carts]
        
        return JsonResponse({'Result' : Result}, status=200)

class CartEditView(View):
    @login_decorator
    def patch(self, request, cart_id):
        try:
            data     = json.loads(request.body)
            quantity = data['product_quantity']
            cart     = Cart.objects.filter(id=cart_id, user_id=request.user)

            cart.update(quantity=quantity)

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

    @login_decorator
    def delete(self, request, cart_id):
        cart = Cart.objects.filter(user=request.user, id=cart_id).delete()
        
        return JsonResponse({'MESSAGE':'NO_CONTENT'}, status=204)