from . import views
from django.urls import path
from django.contrib import admin

app_name = "flights"
urlpatterns = [
    path("",views.index, name="index"),
    path("<int:flight_id>", views.Flight, name="flight"),
    path("<int:flight_id>/book>", views.book, name="book"),
    path("admin/", admin.site.urls)
]
