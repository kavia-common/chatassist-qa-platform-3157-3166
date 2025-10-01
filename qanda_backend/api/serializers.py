from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Chat, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "chat", "role", "content", "created_at", "token_usage"]
        read_only_fields = ["id", "created_at", "token_usage"]


class ChatSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ["id", "title", "owner", "created_at", "messages"]
        read_only_fields = ["id", "owner", "created_at", "messages"]


class AskRequestSerializer(serializers.Serializer):
    """
    Request payload to send a question.
    """
    chat_id = serializers.IntegerField(required=False, help_text="Chat ID to append the message to. If omitted, creates a new chat.")
    prompt = serializers.CharField(help_text="User's question/prompt.")
    title = serializers.CharField(required=False, allow_blank=True, help_text="Optional chat title when creating a new chat.")


class AskResponseSerializer(serializers.Serializer):
    """
    Response payload after asking a question.
    """
    chat = ChatSerializer()
    answer = serializers.CharField(help_text="Assistant response.")
