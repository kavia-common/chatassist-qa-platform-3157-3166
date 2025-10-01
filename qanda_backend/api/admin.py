from django.contrib import admin
from .models import Chat, Message, UserProfile


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "title", "created_at")
    list_filter = ("owner", "created_at")
    search_fields = ("title", "owner__username")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat", "role", "short_content", "created_at")
    list_filter = ("role", "created_at", "chat")
    search_fields = ("content",)

    def short_content(self, obj):
        return (obj.content or "")[:80]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
