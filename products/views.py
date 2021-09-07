from django.http import JsonResponse
from django.views import View

from .models import Category

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