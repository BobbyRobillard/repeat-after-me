from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from website.views import homepage_view

from .forms import ProfileForm
from .models import Profile
from .utils import set_current_profile, delete_profile

import json


@login_required
def homepage_view(request):
    context = {
        "profiles": ["", "", ""]
    }
    return render(request, "macros/homepage.html", context)


@login_required
def set_current_profile_view(request, pk):
    if not set_current_profile(request.user, pk):
        messages.error(request, "You do not own this profile chief.")
    return redirect('website:homepage')


@login_required
def delete_profile_view(request, pk):
    if not delete_profile(request.user, pk):
        messages.error(request, "You do not own this profile chief.")
    return redirect('website:homepage')


@login_required
def add_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            Profile.objects.create(name=form.cleaned_data['name'], user=request.user)
    return redirect('website:homepage')


@login_required
def add_recording(request):
    return redirect('website:homepage')
