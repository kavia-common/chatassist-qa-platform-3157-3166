# API Notes

Endpoints:
- GET /api/health/ -> health check
- GET /api/chats/ -> list chats for demo/current user
- GET /api/history/?chat_id={id} -> message history
- POST /api/ask/ -> body: { "chat_id"?: number, "prompt": string, "title"?: string }
- POST /api/chat/send/ -> alias of /api/ask/ (same body and behavior)

Environment variables:
- OPENAI_API_KEY: required to generate answers (backend-only secret)
- OPENAI_MODEL: optional (default gpt-4o-mini)
- PUBLIC_BACKEND_BASE_URL: public base URL of the backend for frontend to call
- CORS_ALLOWED_ORIGINS: comma-separated allowed frontend origins (e.g., http://localhost:3000)
- DJANGO_SECRET_KEY, DEBUG, ALLOWED_HOSTS, TIME_ZONE, DB_* for database overrides

Frontend alignment:
- Frontend should use API base: ${PUBLIC_BACKEND_BASE_URL}/api
- Do not expose OPENAI_API_KEY in frontend code or environments.

This backend uses LangChain + OpenAI (ChatOpenAI).
