from django.urls import path
from users.views import LoginView, SignupView, test

urlpatterns = [
    path('/signup', SignupView.as_view()),
    path('/login', LoginView.as_view()),
    # path('/test', test.as_view()),
    # path('/test', Test.as_view()),
]