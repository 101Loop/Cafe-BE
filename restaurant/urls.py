from django.urls import path
from . import views


app_name = 'restaurant'

urlpatterns = [
    # ex: api/restaurant/show/item/
    path('show/item/', views.ShowItemView.as_view(), name='Show-Item'),
    # ex: api/restaurant/show/lunchpack/
    path('show/lunchpack/', views.ShowLunchPackView.as_view(), name='Show-Lunch-Pack'),
    # ex: api/restaurant/show/store/
    path('show/store/', views.ShowStoreView.as_view(), name='Show-Store'),
    # ex: api/restaurant/add/item/
    path('add/item/', views.AddItemView.as_view(), name='Add-Item'),
    # ex: api/restaurant/show/tag/
    path('show/tag/', views.ShowTagView.as_view(), name='Show Tag'),
    path('show/section/', views.ShowSectionView.as_view(), name='Show Sections'),
]
