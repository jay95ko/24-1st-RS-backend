import json, re
import bcrypt

from django.http import JsonResponse
from django.views import View

from users.models import User

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

            if data['smscheck']   == 'on':
                is_sms_agree      = 'True'
            else:
                is_sms_agree      = 'False'
                
            if data['emailcheck'] == 'on':
                is_email_agree    = 'True'
            else:
                is_email_agree    = 'False'

            User.objects.create(
                name           = data['name'],
                email          = data['email'],
                password       = decoded_hashed_password,
                is_sms_agree   = is_sms_agree,
                is_email_agree = is_email_agree,
            )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)