from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path("", views.CartDetailView.as_view(), name="detail"),
    path("add/", views.CartAddView.as_view(), name="add"),
    path("add/<slug:slug>/", views.CartAddView.as_view(), name="add_product"),   
]