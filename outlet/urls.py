from django.urls import path

from .views import ListOutletProductView, ListOutletView, RetrieveProductView, ListManagerOutletView

app_name = "outlet"


urlpatterns = [
    path('public/outlet/', ListOutletView.as_view(), name="List Outlets"),
    path('public/<int:outlet__id>/product/', ListOutletProductView.as_view(),
         name="List Outlets"),
    path('public/<int:outlet_id>/<int:product_id>/',
         RetrieveProductView.as_view(),
         name="Retrieve Outlet Product"),
    path('manager/', ListManagerOutletView.as_view(), name="List Managers"),
]
