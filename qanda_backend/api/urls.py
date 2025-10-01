from django.urls import path
from .views import health, list_chats, chat_history, ask

urlpatterns = [
    path('health/', health, name='Health'),
    path('chats/', list_chats, name='ListChats'),
    path('history/', chat_history, name='ChatHistory'),
    path('ask/', ask, name='AskQuestion'),
    # Backward-compatible alias for clients calling /api/chat/send/
    path('chat/send/', ask, name='ChatSend'),
]
