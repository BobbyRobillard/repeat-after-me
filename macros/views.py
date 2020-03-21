from django.contrib.auth.models import User as User

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from website.views import homepage_view

from .forms import ProfileForm
from .models import Profile
from .utils import set_current_profile, delete_profile, toggle_play_mode, check_for_updates, set_update_needed

import json


@login_required
def homepage_view(request):
    context = {
        "profiles": ["", "", ""]
    }
    return render(request, "macros/homepage.html", context)


def toggle_play_mode_view(request, username):
    toggle_play_mode(username)
    set_update_needed(User.objects.get(username=username))
    return redirect('website:homepage')


@login_required
def check_for_updates_view(request):
    return JsonResponse({'updates_waiting': check_for_updates(request.user)})


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
