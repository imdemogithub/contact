from django.contrib import admin
from .models import *

admin.site.site_header = admin.site.site_title = "Contact Manager"
admin.site.register(Master)
admin.site.register(UserProfile)
admin.site.register(Contact)