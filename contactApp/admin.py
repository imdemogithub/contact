from django.contrib import admin
from .models import *

class SuperAdmin(admin.ModelAdmin):
    admin.site.site_header = admin.site.site_title = "Contact Manager"
    list_per_page = 10

# display object name in admin table view
class MasterHeader(admin.ModelAdmin):
    admin.site.site_header = admin.site.site_title
    list_display = list_display_links = ('id', 'Email', 'IsActive')
    list_filter = ('IsActive',)

# display object name in admin table view
class UserProfileHeader(admin.ModelAdmin):
    list_display = list_display_links = ('id', 'FullName', 'Mobile')
    list_filter = ('Country', 'Pincode')

# display object name in admin table view
class ContactHeader(admin.ModelAdmin):
    list_display = list_display_links = ('id', 'FullName', 'Email', 'Mobile', 'Category')
    list_filter = ('Category', 'Country', 'Pincode')

class AutoCreate:
    def __init__(self):

        self.data_model = [
            (Master, MasterHeader),
            (UserProfile, UserProfileHeader),
            (Contact, ContactHeader),
        ]

        # register all models in admin
        for dm in self.data_model:
            #print(dm)
            admin.site.register(dm[0], dm[1])

init = AutoCreate()