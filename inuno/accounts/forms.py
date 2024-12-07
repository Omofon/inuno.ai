from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser


class SignUpForm(forms.ModelForm):
    """Sign up form for Users"""

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Create a password"})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"})
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter your username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password.")
            if not user.is_active:
                raise forms.ValidationError("This account is inactive.")
        return cleaned_data
