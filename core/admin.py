from django.contrib import admin
from .models import ProfileUser,UserFollowing,PostModel,LikeModel

# Register your models here.


admin.site.register(ProfileUser)
admin.site.register(UserFollowing)
admin.site.register(PostModel)
admin.site.register(LikeModel)
