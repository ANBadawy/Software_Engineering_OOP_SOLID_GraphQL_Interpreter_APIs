from django.urls import path
from .views import ComputeValueAPIView

urlpatterns = [
    path('Ingester/', ComputeValueAPIView.as_view(), name='message-ingester'),
]


