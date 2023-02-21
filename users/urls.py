from os import name
from . import views
from django.urls import path

app_name="users"
urlpatterns = [
    path("",views.index, name="index"),
    path("login/",views.login_request, name="login"),
    path("logout/", views.logout_view, name="logout")
]
