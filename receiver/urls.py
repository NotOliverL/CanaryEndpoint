from django.urls import path
from .views import receive_api_call

urlpatterns = [
    path('<str:path>/', receive_api_call, name='receive_api_call'),
]