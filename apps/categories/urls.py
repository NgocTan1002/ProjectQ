from django.urls import path
from . import views

app_name="categories"
urlpattern=[
    path("", views.CategoryListView.as_view(), name="list"),
    path("brand", )
]