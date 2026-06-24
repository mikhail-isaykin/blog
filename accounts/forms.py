from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Profile

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-1', 'placeholder': 'Enter Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control mb-1', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mb-1', 'placeholder': 'Enter Last Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control mb-1', 'placeholder': 'Enter your E-Mail'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control mb-1', 'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control mb-1', 'placeholder': 'Confirm Password'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {
                'class': 'form-control mb-1',
                'placeholder': 'Username',
            }
        )
        self.fields['password'].widget.attrs.update(
            {
                'class': 'form-control mb-1',
                'placeholder': 'Password',
            }
        )


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-1', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-1', 'placeholder': 'Email'}),
        }


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control mb-1'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }
