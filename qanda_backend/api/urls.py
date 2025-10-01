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
    # GET endpoints (with and without trailing slash)
    path('health/', health, name='Health'),
    path('health', health),  # no-slash variant

    path('chats/', list_chats, name='ListChats'),
    path('chats', list_chats),  # no-slash variant

    path('history/', chat_history, name='ChatHistory'),
    path('history', chat_history),  # no-slash variant

    # POST endpoints (with and without trailing slash)
    path('ask/', ask, name='AskQuestion'),
    path('ask', ask),  # no-slash variant

    # Backward-compatible alias for clients calling /api/chat/send/
    path('chat/send/', ask, name='ChatSend'),
    path('chat/send', ask),  # no-slash variant
]
