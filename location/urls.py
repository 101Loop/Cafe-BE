from django.urls import path

from .views import ListCityView, ListCountryView, ListStateView


app_name = "location"


urlpatterns = [
    path('country/', ListCountryView.as_view(), name="country-list"),
    path('state/', ListStateView.as_view(), name="state-list"),
    path('city/', ListCityView.as_view(), name="city-list"),
]
