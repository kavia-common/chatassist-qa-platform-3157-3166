# API Notes

Endpoints:
- GET /api/health/ -> health check
- GET /api/chats/ -> list chats for demo/current user
- GET /api/history/?chat_id={id} -> message history
- POST /api/ask/ -> body: { "chat_id"?: number, "prompt": string, "title"?: string }
- POST /api/chat/send/ -> alias of /api/ask/ (same body and behavior)

Environment variables:
- OPENAI_API_KEY: required to generate answers
- OPENAI_MODEL: optional (default gpt-4o-mini)
- DJANGO_SECRET_KEY, DEBUG, ALLOWED_HOSTS, DB_* for database overrides

This backend uses LangChain + OpenAI (ChatOpenAI).
