import json, re
import bcrypt, jwt
import datetime

from django.http import JsonResponse
from django.views import View

from users.models import User
from my_settings import SECRET_KEY, ALGORITHM
from users.decorator import login_decorator

class SignupView(View):
    def post(self, request):
        try:
            data                = json.loads(request.body)
            name                = data['name']
            email               = data['email']
            password            = data['password']
            repassword          = data['repassword']
            email_validation    = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
            password_validation = re.compile("^.*(?=^.{8,}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%*^&+=]).*$")

            if not (email and password and name and repassword):
                return JsonResponse({"MESSAGE":"EMPTY_VALUE_ERROR"}, status=400)

            if not email_validation.match(email):
                return JsonResponse({"MESSAGE":"EMAIL_VALIDATION_ERROR"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"MESSAGE":"DUPLICATION_ERROR"}, status=400)

            if not password_validation.match(password):
                return JsonResponse({"MESSAGE":"PASSWORD_VALIDATION_ERROR"}, status=400)

            if not password == repassword:
                return JsonResponse({"MESSAGE":"PASSWORD_DO_NOT_MATCH_ERROR"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_password = hashed_password.decode('utf-8')

            User.objects.create(
                name           = data['name'],
                email          = data['email'],
                password       = decoded_hashed_password,
                is_sms_agree   = data['smscheck'],
                is_email_agree = data['emailcheck'],
            )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

class LoginView(View):   
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not (data['email'] and data['password']):
                return JsonResponse({"MESSAGE":"EMPTY_VALUE_ERROR"}, status=400)

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({"MESSAGE":"INVALID_USER"}, status=401)

            user = User.objects.get(email=data['email'])
            if not user.deactivated_at:
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    access_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
                    return JsonResponse({"MESSAGE":"SUCCESS","ACCESS_TOKEN":access_token}, status=201)
                
                return JsonResponse({"MESSAGE":"INVALID_USER"}, status=401)
            
            return JsonResponse({"MESSAGE":"DEACTIVATE_USER"}, status=401)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)

class UserActivateView(View):
    def patch(self, request):
        try:
            data = json.loads(request.body)

            if not (data['email'] and data['password']):
                return JsonResponse({"MESSAGE":"EMPTY_VALUE_ERROR"}, status=400)

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({"MESSAGE":"INVALID_USER"}, status=401)
            
            user = User.objects.get(email=data['email'])
            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                user.update(deactivated_at = None)
                access_token = jwt.encode({'id':user.id}, SECRET_KEY, algorithm=ALGORITHM)
                return JsonResponse({"MESSAGE":"SUCCESS_ACTIVATE","ACCESS_TOKEN":access_token}, status=201)
                
            return JsonResponse({"MESSAGE":"INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)

class UserDetailView(View):
    @login_decorator
    def get(self, request):
        user = request.user
        result = {
            "name"           : user.name,
            "email"          : user.email,
            "is_sms_agree"   : user.is_sms_agree,
            "is_email_agree" : user.is_email_agree,
        }
        return JsonResponse({"Result": result}, status=200)
    
    @login_decorator
    def patch(self, request):
        try:
            data = json.loads(request.body)

            password            = data['password']
            password_validation = re.compile("^.*(?=^.{8,}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%*^&+=]).*$")

            if not data['password']:
                return JsonResponse({"MESSAGE":"EMPTY_VALUE_ERROR"}, status=400)
            
            if not password_validation.match(password):
                return JsonResponse({"MESSAGE":"PASSWORD_VALIDATION_ERROR"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_password = hashed_password.decode('utf-8')
            
            request.user.password        = decoded_hashed_password
            request.user. is_sms_agree   = data['smscheck']
            request.user. is_email_agree = data['emailcheck']
            request.user.save()

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)

    @login_decorator
    def delete(self, request):
        now  = datetime.datetime.now()
        request.user.deactivated_at = now
        request.user.save()

        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
