from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout, name="logout"),
    path("home", views.home, name="home"),
    path("menu/<str:category>", views.menu, name="menu"),
    path("add/<str:name>/<str:category>/<str:price>", views.add, name="add"),
    path("cart", views.cart, name="cart"),
    path("confirm", views.confirm, name="confirm"),
    path("delete/<str:name>/<str:category>/<str:price>", views.delete, name="delete")
]
