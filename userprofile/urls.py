from django.urls import path

from . import views


app_name = "userprofile"


urlpatterns = [
    path('category/', views.ListCategoryView.as_view(), name='list-category'),
    path('profile/', views.UserProfileView.as_view(),
         name="retrieve-update-userprofile"),
]
