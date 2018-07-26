from django.urls import path
from . import views


app_name = 'restaurant'

urlpatterns = [
    path('add/item/', views.AddItemView.as_view(), name='Add-Item'),
    path('show/item/', views.ShowItemView.as_view(), name='Show-Item'),
    path('add/lunchpack/', views.AddLunchPackView.as_view(), name='Add-Lunch-Pack'),
    path('show/lunchpack/', views.ShowLunchPackView.as_view(), name='Show-Lunch-Pack'),
    path('add/store/', views.AddStoreView.as_view(), name='Add-Store'),
    path('show/store/', views.ShowStoreView.as_view(), name='Show-Store'),
]
