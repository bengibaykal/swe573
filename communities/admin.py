from django.contrib import admin

# Register your models here.

from .models import Community
from .models import Post, Post2

admin.site.register(Community)
admin.site.register(Post)
admin.site.register(Post2)

