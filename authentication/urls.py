from django.urls import path

from .views import user_creation_view

urlpatterns = [
    path('register/', user_creation_view.as_view(), name='register'),
]