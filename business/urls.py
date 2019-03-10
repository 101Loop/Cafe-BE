from django.urls import path

from .views import ListBusinessView

app_name = "business"


urlpatterns = [
    path('business/', ListBusinessView.as_view(), name="list-business"),
]
