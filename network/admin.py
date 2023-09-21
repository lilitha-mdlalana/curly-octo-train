from django.contrib import admin

# Register your models here.
from .models import Post,PostLike,User,FollowersCount

admin.site.register(User)
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(FollowersCount)