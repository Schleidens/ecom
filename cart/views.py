from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import View

from .models import Cart, CartItem
from store.models import Product

from store.forms import Quantity


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
        
        context = {
            'items' : cart_items,
            'cart' : cart
        }
        
        return render(request, self.template, context=context)
    