from typing import List, Tuple

from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, AskRequestSerializer, AskResponseSerializer
from .services import OpenAIChatService


@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    """
    Health check endpoint.
    Returns a simple JSON indicating the server status.
    """
    return Response({"message": "Server is up!"})


def _get_or_create_demo_user() -> User:
    """
    Demo mode helper: creates/returns a default user when auth is not configured.
    """
    user, _ = User.objects.get_or_create(username="demo")
    return user


@swagger_auto_schema(
    method="get",
    operation_id="list_chats",
    tags=["Chat"],
    operation_summary="List chats for current user",
    operation_description="Returns all chats for the current user (demo user if auth not configured).",
    responses={200: ChatSerializer(many=True)},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def list_chats(request):
    """
    List chats for the requesting user. In absence of auth, uses a demo user.
    """
    user = request.user if request.user and request.user.is_authenticated else _get_or_create_demo_user()
    chats = Chat.objects.filter(owner=user).order_by("-created_at")
    data = ChatSerializer(chats, many=True).data
    return Response(data)


@swagger_auto_schema(
    method="get",
    operation_id="chat_history",
    tags=["Chat"],
    manual_parameters=[
        openapi.Parameter("chat_id", openapi.IN_QUERY, description="Chat ID", type=openapi.TYPE_INTEGER, required=True)
    ],
    operation_summary="Fetch chat history",
    operation_description="Returns the message history for the specified chat.",
    responses={200: MessageSerializer(many=True)},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def chat_history(request):
    """
    Fetch message history for given chat_id.
    """
    chat_id = request.query_params.get("chat_id")
    if not chat_id:
        return Response({"detail": "chat_id is required"}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user if request.user and request.user.is_authenticated else _get_or_create_demo_user()
    chat = get_object_or_404(Chat, pk=chat_id, owner=user)
    messages = chat.messages.all()
    return Response(MessageSerializer(messages, many=True).data)


@swagger_auto_schema(
    method="post",
    request_body=AskRequestSerializer,
    responses={200: AskResponseSerializer},
    operation_id="ask_question",
    tags=["Chat"],
    operation_summary="Send a question and get an answer",
    operation_description="Creates a message for the user prompt, calls OpenAI via LangChain, stores the assistant reply, and returns the updated chat and answer.",
)
@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic
def ask(request):
    """
    Accepts a prompt and an optional chat_id. If chat_id is absent, a new chat is created.
    Persists the user's message and the assistant's reply using LangChain + OpenAI.
    """
    serializer = AskRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    user = request.user if request.user and request.user.is_authenticated else _get_or_create_demo_user()
    chat: Chat | None = None

    if "chat_id" in data and data["chat_id"] is not None:
        chat = get_object_or_404(Chat, pk=data["chat_id"], owner=user)
    else:
        chat = Chat.objects.create(owner=user, title=data.get("title") or "New Chat")

    # Save user message
    Message.objects.create(chat=chat, role="user", content=data["prompt"])

    # Build history for LLM
    history: List[Tuple[str, str]] = [(m.role, m.content) for m in chat.messages.all().order_by("created_at", "id")]

    # Call OpenAI via LangChain
    chat_service = OpenAIChatService()
    try:
        answer = chat_service.generate_reply(history=history, prompt=data["prompt"])
    except Exception as e:
        return Response({"detail": f"LLM error: {e}"}, status=status.HTTP_502_BAD_GATEWAY)

    # Save assistant message
    Message.objects.create(chat=chat, role="assistant", content=answer)

    response = AskResponseSerializer({"chat": ChatSerializer(chat).data, "answer": answer}).data
    return Response(response, status=status.HTTP_200_OK)
