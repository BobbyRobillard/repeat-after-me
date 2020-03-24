from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from macros.forms import ProfileForm
from macros.utils import get_profiles, get_current_profile, get_settings

import json


@login_required
def homepage_view(request):
    request.session["updates_waiting"] = False
    settings = get_settings(request.user)
    context = {
        "profiles": get_profiles(request.user),
        "profile_form": ProfileForm(),
        "settings": settings,
        "current_profile_recordings": settings.current_profile.get_recordings(),
    }
    return render(request, "website/homepage.html", context)
