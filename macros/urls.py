from django.conf.urls import url, include
from django.urls import path

from . import views
from .views import DeleteProfileView, DeleteRecordingView

# Application Routes (URLs)

app_name = "macros"

urlpatterns = [
    # General Page Views
    url(r"^add-profile$", views.add_profile, name="add_profile"),
    url(r"^get-token$", views.generate_token, name="generate_token"),
    url(r"^save-recording$", views.save_recording, name="save_recording"),
    url(
        r"^download-recording/(?P<token>[\w\-]+)/(?P<key_char>[\w\-]+)/$",
        views.download_recording,
        name="download_recording",
    ),
    url(
        r"^toggle-play-mode/(?P<token>[\w\-]+)/(?P<toggle>\d+)/$",
        views.toggle_play_mode_view,
    ),
    url(r"^start-recording/(?P<token>[\w\-]+)/$", views.start_recording_view),
    url(r"^stop-recording/(?P<token>[\w\-]+)/$", views.stop_recording_view),
    url(r"^sync/(?P<token>[\w\-]+)/$", views.sync_view, name="sync"),
    url(
        r"^set-current-profile/(?P<pk>\d+)/$",
        views.set_current_profile_view,
        name="set_current_profile",
    ),
    url(
        r"^delete-profile/(?P<pk>\d+)/$",
        views.DeleteProfileView.as_view(),
        name="delete_profile",
    ),
    url(
        r"^delete-recording/(?P<pk>\d+)/$",
        views.DeleteRecordingView.as_view(),
        name="delete_recording",
    ),
]
