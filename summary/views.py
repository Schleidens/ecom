from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import View

from .models import Summary

# Create your views here.

class order_history(LoginRequiredMixin, View):
    model = Summary
    template = 'order_history.html'
    
    def get(self, request):
        orders = self.model.objects.filter(customer=request.user)
        
        return render(request, self.template, {'orders': orders})
