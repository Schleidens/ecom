from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

from .models import Cart, CartItem
from store.models import Product

from store.forms import Quantity


#add item to cart feature, use FBV just because it's a request and doesn't require get an post
@login_required
def add_to_cart(request, product_id):
    
    if request.method == 'POST':
        form = Quantity(request.POST)
        if form.is_valid():
            
            #get quantity from form
            quantity = form.cleaned_data['quantity']
            
            #pass product.id from dynamic url as arg to get the single product
            product = get_object_or_404(Product, id=product_id)
            
            #get or create a new cart 
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            #create a cartItem with the product in add it to cart
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
            
            #check if the cartItem was created and create it or change the quantity
            if not item_created:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                cart_item.quantity = quantity
                cart_item.save()
            return redirect('/')
    else:
        form = Quantity()
    
    return redirect(request.path)






    
    