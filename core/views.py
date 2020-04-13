from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import (
    login as auth_login,
    authenticate as auth_authenticate,
    logout as auth_logout,
)
from django.conf import settings
from django.core.exceptions import SuspiciousOperation

from .forms import RegisterForm

from .utils import recaptcha_validation

from macros.models import Settings


# Login
def login(request):
    if request.method == "POST":
        if True:
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password")
                user = auth_authenticate(username=username, password=raw_password)
                auth_login(request, user)
                next_page = request.GET.get("next", "website:homepage_view")
                return redirect(next_page)
        else:
            raise SuspiciousOperation()
    else:
        form = AuthenticationForm()

    context = {"form": form, "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY}
    return render(request, "registration/login_page.html", context)


# Logout
def logout(request):
    auth_logout(request)
    next_page = request.GET.get("next", "website:homepage")
    return redirect(next_page)


# Register a new user
def register(request):
    # Handle new user signup
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data['username'])
            Settings.objects.create(user=user)
            return redirect("website:homepage")
    else:
        form = RegisterForm()

    # Display page to register
    return render(request, "registration/register.html", {"form": form})
