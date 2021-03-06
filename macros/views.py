from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse, HttpResponse
from django.urls import reverse

from django.http import JsonResponse, HttpResponse, Http404

from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import DeleteView, UpdateView, CreateView

from django.utils.decorators import method_decorator

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from website.views import homepage_view

from .forms import ProfileForm, RecordingForm, SettingsForm
from .models import Profile, KeyEvent, MouseEvent, Recording, Settings
from .serializers import KeyEventSerializer, MouseEventSerializer
from .utils import (
    get_settings,
    get_current_profile,
    toggle_play_mode,
    start_recording,
    stop_recording,
    sync,
    get_profiles,
    set_current_profile,
    get_possible_icons,
    get_settings_from_token,
    Http404,
    convert_from_url_safe_key_code
)

import json


@method_decorator(login_required, name="dispatch")
class UpdateSettingsView(UpdateView):
    model = Settings
    form_class = SettingsForm
    template_name_suffix = "_update_form"
    success_url = "/"

    def get_object(self, *args, **kwargs):
        obj = super(UpdateSettingsView, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profiles"] = get_profiles(self.request.user)
        return context

    def form_valid(self, form):
        messages.success(self.request, "Settings were updated successfully!")
        return super().form_valid(form)


@login_required
def stop_showing_sharing(request):
    settings = get_settings(request.user)
    settings.show_social_sharing = False
    settings.save()
    return redirect('website:homepage')


def generate_token(request):
    token = Token.objects.get_or_create(user=request.user)[0]
    context = {
        "token": token,
        "profiles": get_profiles(request.user),
        "settings": get_settings(request.user)
    }
    return render(request, "macros/token.html", context)


@login_required
def quit_tutorial(request):
    try:
        settings = get_settings(request.user)
        settings.offer_tutorial = False
        settings.show_social_sharing = True
        settings.save()
    except Exception as e:
        print(str(e))
    return redirect("website:homepage")


def toggle_play_mode_view(request, token, toggle):
    toggle_play_mode(token, toggle)
    return JsonResponse({}, status=200)


def sync_view(request, token):
    sync(token)
    return JsonResponse({}, status=200)


# ------------------------------------------------------------------------------
# PROFILE RELATED VIEWS
# ------------------------------------------------------------------------------


@method_decorator(login_required, name="dispatch")
class CreateProfileView(CreateView):
    model = Profile
    fields = ["name", "color", "icon"]
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateProfileView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["icons"] = get_possible_icons()
        context["profiles"] = get_profiles(self.request.user)
        context["settings"] = get_settings(self.request.user)
        context["default_colors"] = [
            "#eb2f06",
            "#fa983a",
            "#FFEB3B",
            "#78e08f",
            "#82ccdd",
            "#0088ff",
            "#673AB7",
            "#E91E63",
        ]
        return context


@method_decorator(login_required, name="dispatch")
class DeleteProfileView(DeleteView):
    model = Profile
    success_url = "/"

    def get_object(self, *args, **kwargs):
        obj = super(DeleteProfileView, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def delete(self, *args, **kwargs):
        object = self.get_object()
        # Change user's current profile, only if it is the one being deleted
        try:
            settings = get_settings(self.request.user)
            if settings.current_profile.pk == object.pk:
                profile = get_profiles(settings.user).exclude(pk=object.pk).first()
                settings.current_profile = profile
                settings.save()
        except Exception as outer_error:
            settings.current_profile = None
            settings.save()
            messages.error(
                self.request, "You have no profiles to set as your current profile."
            )

        messages.success(self.request, "Profile Deleted!")
        return super(DeleteProfileView, self).delete(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profiles"] = get_profiles(self.request.user)
        context["settings"] = get_settings(self.request.user)
        return context


@method_decorator(login_required, name="dispatch")
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name_suffix = "_update_form"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profiles"] = get_profiles(self.request.user)
        context["settings"] = get_settings(self.request.user)
        return context

    def get_object(self, *args, **kwargs):
        obj = super(UpdateProfileView, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def form_valid(self, form):
        messages.success(
            self.request, "{0} was updated successfully!".format(self.get_object().name)
        )
        return super().form_valid(form)


@login_required
def set_current_profile_view(request, pk):
    set_current_profile(request.user, pk)
    return redirect("website:homepage")


# ------------------------------------------------------------------------------
# RECORDING RELATED VIEWS
# ------------------------------------------------------------------------------


def save_recording(request):

    form = RecordingForm()

    if not Recording.objects.filter(
        profile=get_current_profile(request.user), is_temp=True
    ).exists():

        messages.error(
            request,
            "You have no temporary recording! Please record one now, then refresh this page!",
        )

    elif request.method == "POST":
        form = RecordingForm(request.POST)
        current_profile = get_current_profile(request.user)
        form.user = request.user
        if form.is_valid():
            rec = Recording.objects.get(is_temp=True, profile=current_profile)
            rec.name = form.cleaned_data["name"]
            rec.key_code = form.cleaned_data["key_code"]
            rec.is_temp = False
            rec.save()
            messages.success(request, "Recording saved to {0}".format(current_profile))
            return redirect("website:homepage")

    return render(
        request,
        "macros/save_recording.html",
        context={
            "profiles": get_profiles(request.user),
            "settings": get_settings(request.user),
            "form": form,
        },
    )


class DeleteRecordingView(DeleteView):
    model = Recording
    success_url = "/"

    def get_object(self, *args, **kwargs):
        obj = super(DeleteRecordingView, self).get_object(*args, **kwargs)
        if not obj.profile.user == self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profiles"] = get_profiles(self.request.user)
        context["settings"] = get_settings(self.request.user)
        return context


def download_recording(request, token, key_char):
    try:
        user = Token.objects.get(key=token).user
        print(str("KEYCODE: " + convert_from_url_safe_key_code(key_char)))
        recording = Recording.objects.get(
            key_code=convert_from_url_safe_key_code(key_char), profile=get_settings(user).current_profile
        )
        events = recording.get_events()

    except Recording.DoesNotExist:
        return HttpResponse(status=404)

    key_event_serializer = KeyEventSerializer(events["key_events"], many=True)
    mouse_event_serializer = MouseEventSerializer(events["mouse_events"], many=True)

    return JsonResponse(
        {"events": key_event_serializer.data + mouse_event_serializer.data}, status=200
    )


def start_recording_view(request, token):
    try:
        if get_settings_from_token(token).play_mode:
            start_recording(token)
        else:
            return JsonResponse({"errors": "Play mode is not active"}, status=404)
    except Exception as e:
        return JsonResponse({"errors": "Invalid token"}, status=404)
    return JsonResponse({}, status=200)


@csrf_exempt
@api_view(["GET", "POST", "PUT", "DELETE"])
def stop_recording_view(request, token):
    user = Token.objects.get(key=token).user

    errors_exist = False
    errors = {"key_event_errors": [], "mouse_event_errors": []}

    settings = get_settings_from_token(token)

    # Delete temp recordings
    Recording.objects.filter(
        profile=get_current_profile(settings.user),
        is_temp=True
    ).delete()

    # Create new recording to save actions to.
    # New recordings save to the current profile
    new_recording = Recording.objects.create(
        profile=get_current_profile(user),
        name="temp",
        is_temp=True,
        key_code=settings.quick_play_key
    )

    try:
        # Serialize  & save the incoming recording's key events
        for json_encoded_event in request.data["key_events"]:
            new_event = KeyEvent.objects.create(recording=new_recording)
            serializer = KeyEventSerializer(new_event, json_encoded_event)
            if not serializer.is_valid():
                errors["key_event_errors"].append(serializer.errors)
                errors_exist = True
            serializer.save()

        # Serialize  & save the incoming recording's mouse events
        for json_encoded_event in request.data["mouse_events"]:
            new_event = MouseEvent.objects.create(recording=new_recording)
            serializer = MouseEventSerializer(new_event, json_encoded_event)
            if not serializer.is_valid():
                errors["mouse_event_errors"].append(serializer.errors)
                errors_exist = True
            serializer.save()
    except Exception as e:
        print(str(e))

    # If errors exist, report them
    if errors_exist:
        return JsonResponse(errors, status=400)

    # Everything went good, no erros exist
    stop_recording(user)
    return JsonResponse({}, status=200)
