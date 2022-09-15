from django.contrib import admin
from .models import Status, LikeDislikeTweet, LikeDislikeComment

admin.site.register(Status)
admin.site.register(LikeDislikeTweet)
admin.site.register(LikeDislikeComment)

