from django.contrib import admin

from .models import *

admin.site.register(Settings)
admin.site.register(Profile)
admin.site.register(Recording)
admin.site.register(MouseEvent)
admin.site.register(KeyEvent)
# Register your models here.
