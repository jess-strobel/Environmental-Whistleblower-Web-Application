from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="whistleblowingapp"),
    path("logout", views.logoutview, name="logout"),
]