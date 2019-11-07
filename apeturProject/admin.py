from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import *
# Register your models here.

admin.site.register(Client)
admin.site.register(Photographer)
admin.site.register(Address)
admin.site.register(Event_Type)
admin.site.register(File)
admin.site.register(Schedule)
admin.site.register(Event)
