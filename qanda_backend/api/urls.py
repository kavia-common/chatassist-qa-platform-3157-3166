from django.urls import path
from .views import health, list_chats, chat_history, ask

# Note: These routes are included under /api/ via config/urls.py (path("api/", include("api.urls")))
# Therefore, the effective paths are:
# - /api/health/
# - /api/chats/
# - /api/history/
# - /api/ask/ (canonical)
# - /api/chat/send/ (alias to /api/ask/)
urlpatterns = [
    path('health/', health, name='Health'),
    path('chats/', list_chats, name='ListChats'),
    path('history/', chat_history, name='ChatHistory'),
    path('ask/', ask, name='AskQuestion'),
    # Backward-compatible alias for clients calling /api/chat/send/
    path('chat/send/', ask, name='ChatSend'),
]
