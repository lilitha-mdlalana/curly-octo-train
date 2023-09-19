from django.contrib import admin

# Register your models here.
from .models import Post,PostLike,User

admin.site.register(User)
admin.site.register(Post)
admin.site.register(PostLike)