from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from macros.forms import ProfileForm
from macros.utils import get_profiles, get_current_profile

import json


@login_required
def homepage_view(request):
    context = {
        "profiles": get_profiles(request.user),
        "profile_form": ProfileForm(),
        "current_profile_recordings": get_current_profile(request.user).get_recordings()
    }
    return render(request, "website/homepage.html", context)
