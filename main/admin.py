from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Community)
admin.site.register(CommunityItem)
admin.site.register(CommunityItemGroup)
admin.site.register(CommunityItemGroupThrough)