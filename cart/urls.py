from django.urls import path

from .views import add_to_cart, cart_view, remove_from_cart, handle_payment


urlpatterns = [
    path('cart/', cart_view.as_view(), name='cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:cart_item_id>/', remove_from_cart, name='remove-from-cart'),
    path('handle-payment/', handle_payment, name='handle-payment')
]