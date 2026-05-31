from django.contrib import admin

from .models import BlogPost, Item

admin.site.register(Item)
admin.site.register(BlogPost)
