from django.contrib.auth.models import User as User

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import DeleteView

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.parsers import JSONParser

from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view

from website.views import homepage_view

from .forms import ProfileForm
from .models import Profile, KeyEvent, MouseEvent, Recording
from .utils import (
    get_settings,
    get_current_profile,
    delete_profile,
    toggle_play_mode,
    start_recording,
)

from macros.serializers import KeyEventSerializer, MouseEventSerializer

import json


@login_required
def homepage_view(request):
    return render(request, "macros/homepage.html")


def generate_token(request):
    token = Token.objects.get_or_create(user=request.user)[0]
    context = {
        "token": token
    }
    return render(request, "macros/token.html", context)


def toggle_play_mode_view(request, token, toggle):
    toggle_play_mode(token, toggle)
    return JsonResponse({}, status=200)


def start_recording_view(request, token):
    start_recording(token)
    return JsonResponse({}, status=200)


@login_required
def set_current_profile_view(request, pk):
    if not set_current_profile(request.user, pk):
        messages.error(request, "You do not own this profile chief.")
    return redirect("website:homepage")


class DeleteProfileView(DeleteView):
    model = Profile
    success_url = "/"


class DeleteRecordingView(DeleteView):
    model = Recording
    success_url = "/"


@login_required
def add_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            Profile.objects.create(name=form.cleaned_data["name"], user=request.user)
    return redirect("website:homepage")


@login_required
def add_recording(request):
    return redirect("website:homepage")


def download_recording(request, token, key_char):
    try:
        user = Token.objects.get(key=token).user
        recording = Recording.objects.get(
            key_code=key_char,
            profile=get_settings(user).current_profile
        )
        events = recording.get_events()

    except Recording.DoesNotExist:
        return HttpResponse(status=404)

    key_event_serializer = KeyEventSerializer(events['key_events'], many=True)
    mouse_event_serializer = MouseEventSerializer(events['mouse_events'], many=True)

    return JsonResponse({"events": key_event_serializer.data + mouse_event_serializer.data}, status=200)


@csrf_exempt
@api_view(["GET", "POST", "PUT", "DELETE"])
def stop_recording(request, token):
    user = Token.objects.get(key=token).user

    errors_exist = False
    errors = {"key_event_errors": [], "mouse_event_errors": []}

    # Create new recording to save action to.
    # New recordings save to the current profile
    new_recording = Recording.objects.create(
        profile=get_current_profile(user), name="test", key_code="b"
    )

    # Serialize the incoming recording
    for json_encoded_event in request.data["key_events"]:
        new_event = KeyEvent.objects.create(recording=new_recording)
        serializer = KeyEventSerializer(new_event, json_encoded_event)
        # Event error checking
        if serializer.is_valid():
            serializer.save()
        else:
            errors["key_event_errors"].append(serializer.errors)
            errors_exist = True

    for json_encoded_event in request.data["mouse_events"]:
        new_event = MouseEvent.objects.create(recording=new_recording)
        serializer = MouseEventSerializer(new_event, json_encoded_event)
        # Event error checking
        if serializer.is_valid():
            serializer.save()
        else:
            errors["mouse_event_errors"].append(serializer.errors)
            errors_exist = True

    # If errors exist, report them
    if errors_exist:
        return JsonResponse(errors, status=400)

    # Everything went good, no errors exist
    return JsonResponse({"Mood": "Good in the hood!"}, status=200)
