from django.urls import path
from users.views import LoginView, SignupView

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/login', LoginView.as_view()),
]