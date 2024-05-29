from django.contrib import admin
from .models import Todo, Notification

# Register your models here.
admin.site.register(Todo)
admin.site.register(Notification)
