from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extends Django's built-in User with additional fields if needed.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self) -> str:
        return f"UserProfile({self.user.username})"


class Chat(models.Model):
    """
    Represents a chat session owned by a user.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats")
    title = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        base = self.title or f"Chat {self.pk}"
        return f"{base} (owner={self.owner.username})"


class Message(models.Model):
    """
    A message in a chat. role: 'user' for user prompts, 'assistant' for model replies, 'system' optional.
    """
    ROLE_CHOICES = (
        ("user", "User"),
        ("assistant", "Assistant"),
        ("system", "System"),
    )
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=16, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    token_usage = models.IntegerField(null=True, blank=True, help_text="Optional token usage for the message")

    class Meta:
        ordering = ["created_at", "id"]

    def __str__(self) -> str:
        return f"[{self.role}] {self.content[:40]}..."
