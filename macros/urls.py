from django.conf.urls import url, include

from . import views
from .views import DeleteProfileView, DeleteRecordingView

# Application Routes (URLs)

app_name = "macros"

urlpatterns = [
    # General Page Views
    url(r"^add-profile$", views.add_profile, name="add_profile"),
    url(r"^get-token$", views.generate_token, name="generate_token"),
    url(r"^add-recording$", views.add_recording, name="add_recording"),
    url(
        r"^download-recording/(?P<key_char>[\w\-]+)/$",
        views.download_recording,
        name="download_recording",
    ),
    url(r"^upload-recording$", views.upload_recording, name="upload_recording"),
    url(r"^check-for-updates$", views.check_for_updates, name="check_for_updates"),
    url(
        r"^toggle-play-mode/(?P<username>[\w\-]+)/(?P<toggle>\d+)/$",
        views.toggle_play_mode_view,
        name="toggle_play_mode",
    ),
    url(
        r"^toggle-recording/(?P<token>[\w\-]+)/(?P<toggle>\d+)/$",
        views.toggle_recording_view,
        name="toggle_recording",
    ),
    url(r"^stop-recording$", views.stop_recording, name="stop_recording"),
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
