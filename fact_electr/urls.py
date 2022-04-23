from django.urls import URLPattern, path
from .views import GenerarComprobanteApiView

urlpatterns=[
    path('generar-comprobante/', GenerarComprobanteApiView.as_view()),
]