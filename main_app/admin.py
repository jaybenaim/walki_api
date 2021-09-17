from django.contrib import admin
from main_app.models import Event, Pet, Profile

# Register your models here.
admin.site.register(Pet)
admin.site.register(Event)
admin.site.register(Profile)