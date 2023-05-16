from django import forms


class Quantity(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'style' : 'width: 70px;'
    }))