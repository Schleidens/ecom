from django.shortcuts import render

from django.views.generic import View

from .models import (
    Product
)


# Create your views here.

class home_page(View):
    model = Product
    template = 'home_page.html'
    
    def get(self, request):
        product = self.model.objects.all()
        
        return render(request, self.template, {'products': product})
    
    def post(self, request):
        pass


