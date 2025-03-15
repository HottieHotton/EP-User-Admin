from django.urls import path
from . import views
from .views import home, object_detail

urlpatterns = [
    path('', home, name='home'),
    path('list/shipments/', views.shipments_view, name='shipments_list'),
    path('list/addresses/', views.addresses_view, name='addresses_list'),
    path('list/parcels/', views.parcels_view, name='parcels_list'),
    path('<str:obj_type>/<str:obj_id>/', object_detail, name='detail'),
]

