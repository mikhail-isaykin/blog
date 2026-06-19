from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        
    remember_me = forms.BooleanField(required=False)