from django.urls import path

from .views import ListCategoryView


app_name = "product"


urlpatterns = [
    path('category/', ListCategoryView.as_view(), name='category-list'),
]
