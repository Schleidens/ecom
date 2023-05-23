from django.shortcuts import render, redirect

from django.views.generic import View

from django.contrib.auth import login, authenticate

from .forms import createUserForm, loginUserForm


# Create your views here.
class user_creation_view(View):
    form = createUserForm
    template = 'user_creation_view.html'
    
    def get(self, request):
        
        if request.user.is_authenticated:
            return redirect('home-page')
        else:
            form = self.form()
            
            return render(request, self.template, {'form': form})
    
    def post(self, request):
        form = self.form(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            return redirect('home-page')
        return render(request, self.template, {'form': form})
    
    
#view for user login with loginUserForm, CBVs
class user_login_view(View):
    login_form = loginUserForm
    template = 'user_login_view.html'
    message = ''
    
    def get(self, request):
        
        if request.user.is_authenticated:
            return redirect('home-page')
        else:
            form = self.login_form()   
            
            return render(request, self.template, {'form': form})
    
    def post(self, request):
        form = self.login_form(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(
                username = username,
                password = password
            )
            
            if user is not None:
                login(request, user)
                
                return redirect('home-page')
            
        message = 'Username or Password incorrect'
            
        context = {
            'form': form,
            'message' : message
        }
        return render(request, self.template, context=context)