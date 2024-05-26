from django.urls import path
from accounts_app.views import login_view, signup_view, home

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("", home, name="home"),
]
