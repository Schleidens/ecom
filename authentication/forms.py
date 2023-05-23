from django import forms
from django.forms import TextInput, EmailInput

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class createUserForm(UserCreationForm):
    #specify password for having access to his widget
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )
    
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        
        # add widgets for fields from user_model
        widgets = {
            'username' : TextInput(attrs={
                'class' : 'form-control'
            }),
            
            'email' : EmailInput(attrs={
                'class' : 'form-control'
            }),
            
            'first_name' : TextInput(attrs={
                'class' : 'form-control'
            }),
            
            'last_name' : TextInput(attrs={
                'class' : 'form-control'
            })
        }
        
#form for login user view
class loginUserForm(forms.Form):
    username = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Username'
        )
    
    password =  forms.CharField(
        max_length=30,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password'
        )