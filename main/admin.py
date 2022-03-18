from django.contrib import admin

# Register your models here.
from .models import Community, CommunityItem
admin.site.register(Community)
admin.site.register(CommunityItem)
