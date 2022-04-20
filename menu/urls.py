from django.urls import path
from .views import PedidoApiView, PlatoApiView, StockApiView, AgregarDetallePedidoApiView

urlpatterns=[
    path('', PlatoApiView.as_view()),
    path('stock/', StockApiView.as_view()),
    path('pedido/', PedidoApiView.as_view()),
    path('agregar-detalle/',AgregarDetallePedidoApiView.as_view())
]
