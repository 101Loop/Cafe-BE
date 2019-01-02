from django.urls import path

from .views import RetrieveOutletView
from .views import ListOutletProductView, ListOutletView, RetrieveProductView
from .views import ListOutletServiceableAreaView, ListManagerOutletView

app_name = "outlet"


urlpatterns = [
    path('public/outlet/', ListOutletView.as_view(), name="List Outlets"),
    path('public/outlet/<int:pk>/', RetrieveOutletView.as_view(),
         name="outlet-detail"),
    path('public/<int:outlet__id>/product/', ListOutletProductView.as_view(),
         name="List Outlets"),
    path('public/<int:outlet__id>/area/',
         ListOutletServiceableAreaView.as_view(),
         name="List Serviceable Area"),
    path('public/<int:outlet_id>/<int:product_id>/',
         RetrieveProductView.as_view(),
         name="Retrieve Outlet Product"),
    path('manager/outlet/', ListManagerOutletView.as_view(),
         name="ListOutlet-Manager"),
]
