from django.contrib import admin
from restapp.models import PostCardIDEvent
# Register your models here.

@admin.register(PostCardIDEvent)
class PostCardIDEventAdmin(admin.ModelAdmin):
    list_display = ['id', "cardID"]

