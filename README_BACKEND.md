# Q&A Chat Backend (Django)

Run locally:
1. Create virtualenv and install dependencies
2. Copy .env.example to .env and set OPENAI_API_KEY
3. Run migrations
4. Start server

Commands:
- pip install -r qanda_backend/requirements.txt
- cd qanda_backend
- cp .env.example .env
- python manage.py migrate
- python manage.py runserver

Docs:
- Swagger UI: /docs
- Redoc: /redoc

Key endpoints (prefixed with /api):
- GET /health/
- GET /chats/
- GET /history/?chat_id={id}
- POST /ask/ { chat_id?, prompt, title? }
