from django.shortcuts import render,  redirect, get_object_or_404

# Create your views here.

from .models import Cart, CartItem
from store.models import Product

from store.forms import Quantity


#add item to cart feature, use FBV just because it's a request and doesn't require get an post
def add_to_cart(request, product_id):
    
    if request.method == 'POST':
        
        #get the current product
        product =  get_object_or_404(Product, id=product_id)
        
        #get the quantity value
        #quantity = request.POST.get('quantity')
        
        # Get the user's cart or create a new one if it doesn't exist
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Check if the item is already in the cart
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
            
        return redirect('home-page')
    
    