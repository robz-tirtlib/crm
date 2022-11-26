from django.forms import ModelForm, HiddenInput, EmailField
from .models import Order, Customer

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'product', 'status']
        widgets = {'customer': HiddenInput()}


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email']


class ProfileForm(ModelForm):
    class Meta:
        model = Customer
        exclude = ['user']


class CreateUserForm(UserCreationForm):
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'email': None,
            'username': None,
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
