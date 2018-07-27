from django.urls import path
from . import views


app_name = 'restaurant'

urlpatterns = [
    path('show/item/', views.ShowItemView.as_view(), name='Show-Item'),
    path('show/lunchpack/', views.ShowLunchPackView.as_view(), name='Show-Lunch-Pack'),
    path('show/store/', views.ShowStoreView.as_view(), name='Show-Store'),
]
