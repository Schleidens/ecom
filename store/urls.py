from django.urls import path

from .views import (
    home_page,
    category_page,
    product_page,
    request_wishlist,
    wishlist_page
)


urlpatterns = [
    path('', home_page.as_view(), name='home-page'),
    path('<str:slug>', category_page.as_view(), name='category'),
    #product page url passing two dynamic value, category and product
    path('<slug:category>/<slug:product>', product_page.as_view(), name='product'),
    #wishlist form action link for request
    path('request-wishlist/', request_wishlist, name='request-wishlist'),
    #wishlist page
    path('wishlist/', wishlist_page.as_view(), name='wishlist')
]