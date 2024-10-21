from django import forms
from .models import RegisterUser

class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = RegisterUser
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'date_of_birth']
        widgets = {
            'password': forms.PasswordInput(),  # Ensure password field is displayed properly
        }
