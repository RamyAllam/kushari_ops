from django.contrib import admin

# Register your models here.
from .models import servers, location


admin.site.register(servers)
admin.site.register(location)
