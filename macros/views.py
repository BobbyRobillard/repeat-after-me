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
from .utils import (set_current_profile, delete_profile, toggle_play_mode,
                    updates_waiting, set_update_needed, toggle_recording)

import json


@login_required
def homepage_view(request):
    context = {
        "profiles": ["", "", ""]
    }
    return render(request, "macros/homepage.html", context)


def toggle_play_mode_view(request, username, toggle):
    toggle_play_mode(username, toggle)
    set_update_needed(User.objects.get(username=username))
    return redirect('website:homepage')


def toggle_recording_view(request, username, toggle):
    toggle_recording(username, toggle)
    set_update_needed(User.objects.get(username=username))
    return redirect('website:homepage')


@login_required
def check_for_updates_view(request):
    return JsonResponse({'updates_waiting': updates_waiting(request.user)})


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


@login_required
def upload_recording(request, username):
    user = User.objects.get(username=username)
    recording_id = request.SESSION['current_recording_id']
    return redirect('website:homepage')
