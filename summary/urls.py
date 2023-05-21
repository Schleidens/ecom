from django.urls import path

from .views import order_history

urlpatterns = [
    path('summary/', order_history.as_view(), name='summary'),
]