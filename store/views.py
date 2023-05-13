from django.shortcuts import render, get_object_or_404

from django.views.generic import View

from .models import (
    Product,
    Category
)


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


