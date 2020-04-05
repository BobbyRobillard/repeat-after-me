from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from macros.forms import ProfileForm
from macros.utils import get_profiles, get_settings


@login_required
def homepage_view(request):
    try:
        settings = get_settings(request.user)
    except Exception as e:
        return redirect('macros:setup_settings')
    settings.updates_needed = False
    settings.save()
    context = {
        "profiles": get_profiles(request.user),
        "profile_form": ProfileForm(),
        "settings": settings,
    }
    return render(request, "website/homepage.html", context)
