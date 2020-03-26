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
    toggle_recording,
)

from macros.serializers import KeyEventSerializer, MouseEventSerializer

import json


@login_required
def homepage_view(request):
    return render(request, "macros/homepage.html")


def room(request, room_name):
    return render(request, 'macros/room.html', {
        'room_name': room_name
    })


def generate_token(request):
    token = Token.objects.get_or_create(user=request.user)[0]
    context = {
        "token": token
    }
    return render(request, "macros/token.html", context)


def download_recording(request, key_char):
    try:
        recording = Recording.objects.get(
            key_code=key_char, profile=get_settings(request.user).current_profile
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
            "mouse_events": mouse_event_serializer.data,
        },
        safe=False,
    )


def toggle_play_mode_view(request, token, toggle):
    toggle_play_mode(token, toggle)
    return redirect("website:homepage")


def toggle_recording_view(request, token, toggle):
    toggle_recording(token, toggle)
    return redirect("website:homepage")


@csrf_exempt
@api_view(["GET", "PUT", "DELETE"])
def stop_recording(request):
    user = User.objects.get(pk=1)

    errors_exist = False
    errors = {"key_event_errors": [], "mouse_event_errors": []}

    # Create new recording to save action to.
    # New recordings save to the current profile
    new_recording = Recording.objects.create(
        profile=get_current_profile(user), name="test", key_code="a"
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


@login_required
def check_for_updates(request):
    return JsonResponse({"updates_needed": get_settings(request.user).updates_needed})


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
def delete_profile_view(request, pk):
    if not delete_profile(request.user, pk):
        messages.error(request, "You do not own this profile chief.")
    return redirect("website:homepage")


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


@login_required
def upload_recording(request, username):
    user = User.objects.get(username=username)
    recording_id = request.session["current_recording_id"]
    return redirect("website:homepage")
