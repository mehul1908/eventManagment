from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Event)
admin.site.register(models.Participant)
admin.site.register(models.Users)