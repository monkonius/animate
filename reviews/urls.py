from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("anime/<int:anime_id>", views.anime, name="anime"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]