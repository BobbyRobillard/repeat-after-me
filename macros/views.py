from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from website.views import homepage_view

from .forms import ProfileForm
from .models import Profile

import json


@login_required
def homepage_view(request):
    context = {
        "profiles": ["", "", ""]
    }
    return render(request, "macros/homepage.html", context)


@login_required
def add_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            Profile.objects.create(name=form.cleaned_data['name'], user=request.user)
    return redirect('website:homepage')
