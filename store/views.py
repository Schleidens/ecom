from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import View

from .models import (
    Product,
    Category,
    Wishlist
)

from .forms import Quantity


# Create your views here.

class home_page(View):
    product_model = Product
    category_model = Category
    template = 'home_page.html'
    
    def get(self, request):
        product = self.product_model.objects.all()
        category = self.category_model.objects.all()
        
        context = {
            'products' : product,
            'categories' : category
        }
        
        return render(request, self.template, context=context)
    
    def post(self, request):
        pass
    
class category_page(View):
    product_model = Product
    category_model = Category
    template = 'category_page.html'
    
    def get(self, *args, **kwargs):
        category = get_object_or_404(self.category_model, slug=kwargs['slug'])
        product = Product.objects.filter(category=category)
        
        context = {
            'category' : category,
            'products' : product
        }
        
        return render(self.request, self.template, context=context)
    
class product_page(View):
    product_model = Product
    category_model = Category
    form = Quantity
    template = 'product_page.html'
    
    def get(self, *args, **kwargs):
        category = get_object_or_404(self.category_model, slug=kwargs['category'])
        product = get_object_or_404(self.product_model, category=category, slug=kwargs['product'])
        wishlist = Wishlist.objects.filter(user=self.request.user, product=product).exists()
        
        form = self.form()
        
        context = {
            'product' : product,
            'form' : form,
            'is_in_wishlist' : wishlist
        }
        
        return render(self.request, self.template, context=context)

#view to handle the add or remove to wishlist request FBV 
def request_wishlist(request):
    
    if request.method == 'POST':
        
        #get product id and action from template form in post request
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        
        #pass the product_id to get the single product
        product = get_object_or_404(Product, id=product_id)
        
        #verify if this item already exist in the current user wishlist
        is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
        
        if action == 'add':
           Wishlist.objects.create(user=request.user, product=product)
        elif action == 'remove':
            if is_in_wishlist:
                this_wishlist_item = get_object_or_404(Wishlist, user=request.user, product=product)
                this_wishlist_item.delete()
            
            return redirect('home-page')
        return redirect('home-page')