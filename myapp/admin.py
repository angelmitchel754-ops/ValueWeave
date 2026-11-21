from django.contrib import admin
from .models import Profile, Contribution, Confirmation

admin.site.register(Profile)
admin.site.register(Contribution)
admin.site.register(Confirmation)