from django.urls import include, path

from .views import ListOutletProductView, ListOutletView

app_name = "outlet"


urlpatterns = [
    path('public/outlet/', ListOutletView.as_view(), name="List Outlets"),
    path('public/<int:outlet__id>/product/', ListOutletProductView.as_view(),
         name="List Outlets"),
]
