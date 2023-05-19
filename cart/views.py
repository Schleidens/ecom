from django.conf import settings

from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import View

from .models import Cart, CartItem
from store.models import Product

from store.forms import Quantity

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

from decimal import Decimal


# Create your views here.




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
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.quantity = quantity
                cart_item.save()
            return redirect('cart')
    else:
        form = Quantity()
    
    return redirect(request.path)

#remove item from cart FBV
@login_required
def remove_from_cart(request, cart_item_id):
    
    if request.method == 'POST':
            
        #get the cart item by passing the cart_item_id from the dynamic link
        cart_item = get_object_or_404(CartItem, id=cart_item_id)

        if cart_item:
            cart_item.delete()
            
            return redirect('cart')
        
        return redirect('home-page')


#Cart view
class cart_view(LoginRequiredMixin, View):
    cart_model = Cart
    cart_item_model = CartItem
    template = 'cart_view.html'
    
    def get(self, request):
        
        #get the cart
        cart =  get_object_or_404(self.cart_model, user=request.user)
        
        #get the items in cart
        cart_items = self.cart_item_model.objects.filter(cart=cart)
        
        #initialize total price
        cart_total_price = 0
        
        #calculate total price for all cart_items
        for item in cart_items:
            price = item.product.price
            quantity = item.quantity
            
            #assign the final price
            cart_total_price += price * quantity
            
        
        context = {
            'items' : cart_items,
            'cart' : cart,
            'cart_total_price' : cart_total_price,
            'STRIPE_PUBLISHABLE_KEY' : settings.STRIPE_PUBLISHABLE_KEY,
            'stripe_price' : int(Decimal(cart_total_price) * 100)
        }
        
        return render(request, self.template, context=context)
    
    
#handle payment process with stripe with FBV
def handle_payment(request):
    
    #get the cart
    cart =  get_object_or_404(Cart, user=request.user)
    
    #get the items in cart
    cart_items = CartItem.objects.filter(cart=cart)
    
    #initialize total price
    cart_total_price = 0
    
    #calculate total price for all cart_items
    for item in cart_items:
        price = item.product.price
        quantity = item.quantity
        
        #assign the final price
        cart_total_price += price * quantity
    
    #handle the payment process on post request
    if request.method == 'POST':
        token = request.POST['stripeToken']
        amount = int(Decimal(cart_total_price) * 100)
        
        try:
            charge = stripe.Charge.create(
                amount = amount,
                currency = 'usd',
                source = token
            )
            
            #delete all items in cart once payment done
            cart_items.delete()
            
            return redirect('cart')
        except stripe.error.CardError as e:
            error_message = e.error.message
            
            return redirect('home-page')