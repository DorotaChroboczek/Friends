from django.contrib import admin

from .models import Tweet


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'image')
    search_fields = ['user__username', 'user__email']
