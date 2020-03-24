from django.contrib.auth.models import User as User

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.parsers import JSONParser

from website.views import homepage_view

from .forms import ProfileForm
from .models import Profile, KeyEvent, MouseEvent, Recording
from .utils import (get_settings, get_current_profile, delete_profile, toggle_play_mode, toggle_recording)

from macros.serializers import KeyEventSerializer, MouseEventSerializer

import json


@login_required
def homepage_view(request):
    context = {
        "profiles": ["", "", ""]
    }
    return render(request, "macros/homepage.html", context)


def download_recording(request, key_char):
    try:
        recording = Recording.objects.get(
            key_code=key_char,
            profile=get_settings(request.user).current_profile
        )
        key_events = KeyEvent.objects.filter(recording=recording)
        mouse_events = MouseEvent.objects.filter(recording=recording)
    except Recording.DoesNotExist:
        return HttpResponse(status=404)

    key_event_serializer = KeyEventSerializer(key_events, many=True)
    mouse_event_serializer = MouseEventSerializer(mouse_events, many=True)

    return JsonResponse(
        {
            "key_events": key_event_serializer.data,
            "mouse_events": mouse_event_serializer.data
        },
        safe=False
    )


def toggle_play_mode_view(request, username, toggle):
    toggle_play_mode(username, toggle)
    request.session['updates_waiting'] = True
    return redirect('website:homepage')


def toggle_recording_view(request, username, toggle):
    toggle_recording(username, toggle)
    request.session['updates_waiting'] = True
    return redirect('website:homepage')


@login_required
def check_for_updates(request):
    print("STATUS: " + str(request.session['updates_waiting']))
    if request.session['updates_waiting']:
        request.session['updates_waiting'] = False
        return JsonResponse({'updates_waiting': True})
    return JsonResponse({'updates_waiting': False})


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
    recording_id = request.session['current_recording_id']
    return redirect('website:homepage')
