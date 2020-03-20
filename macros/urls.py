from django.conf.urls import url, include

from . import views

# Application Routes (URLs)

app_name = 'macros'

urlpatterns = [
    	# General Page Views
		url(r'^add-profile$', views.add_profile, name='add_profile'),
		url(r'^add-recording$', views.add_recording, name='add_recording'),
		url(r'^set-current-profile/(?P<pk>\d+)/$', views.set_current_profile_view, name='set_current_profile'),
		url(r'^delete-profile/(?P<pk>\d+)/$', views.delete_profile_view, name='delete_profile'),
]
