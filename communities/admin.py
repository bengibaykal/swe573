from django.contrib import admin

# Register your models here.

from .models import Community
from .models import Post, Post2, Field, DataType, DataTypeObject

admin.site.register(Community)
admin.site.register(Post)
admin.site.register(Post2)
admin.site.register(Field)
admin.site.register(DataType)
admin.site.register(DataTypeObject)

