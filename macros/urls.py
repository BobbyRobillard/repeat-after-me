from django.conf.urls import url, include

from . import views

# Application Routes (URLs)

app_name = 'macros'

urlpatterns = [
    	# General Page Views
		url(r'^add-profile$', views.add_profile, name='add_profile'),
]
