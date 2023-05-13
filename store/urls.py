from django.urls import path

from .views import (
    home_page,
    category_page
)


urlpatterns = [
    path('', home_page.as_view(), name='home-page'),
    path('<str:slug>', category_page.as_view(), name='category')
]