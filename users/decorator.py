import jwt, json, requests

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from my_settings import ALGORITHM, SECRET_KEY
from users.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            print('token', access_token)
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
            print('payload', payload)
            request.user = User.objects.get(id=payload['id'])

        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE':'INVALID_TOKEN'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=400)

        return func(self, request, *args, **kwargs)
    return wrapper