from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from .forms import LoginForm, SignUpForm


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect("/")

    next_url = request.GET.get("next", None)
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(next_url or "/")
    context = {
        "form": form,
        "title": "Login",
    }
    return render(request, "accounts/login.html", context)


def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect("/")

    next_url = request.GET.get("next", None)
    form = SignUpForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data["password"]
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        if new_user:
            login(request, new_user)
            return redirect(next_url or "/")

    context = {
        "form": form,
        "title": "Sign Up",
    }
    return render(request, "accounts/signup.html", context)


def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect("/")


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """Display the user profile."""
        user = request.user
        return render(request, "accounts/user_profile.html", {"user": user})

    def post(self, request, *args, **kwargs):
        """Update user profile."""
        user = request.user
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.email = request.POST.get("email", user.email)
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("accounts:user_profile")


class DeleteUserView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        """Delete user account."""
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect("home")
