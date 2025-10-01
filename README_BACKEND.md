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

Notes on routes:
- Canonical chat send endpoint is POST /api/ask/
- For compatibility with some clients, POST /api/chat/send/ is provided as an alias to /api/ask/ (same request/response schema)

Examples:
- POST /api/ask/
  body: { "prompt": "Hello?", "title": "My Chat" }
- POST /api/chat/send/
  body: { "prompt": "Hello?", "title": "My Chat" }

Troubleshooting "Cannot POST /api/chat/send/":
- This message typically comes from a frontend dev server or proxy (not Django/DRF). It means your request isn’t reaching Django.
- Ensure you are posting to the backend host/port where Django runs (e.g., :3001), not the frontend host/port (:3000).
- In this environment the backend is available at:
  - Docs: https://vscode-internal-16277-beta.beta01.cloud.kavia.ai:3001/docs
  - API base: https://vscode-internal-16277-beta.beta01.cloud.kavia.ai:3001/api/
- Test with curl (alias route):
  curl -i -X POST https://vscode-internal-16277-beta.beta01.cloud.kavia.ai:3001/api/chat/send/ \
    -H "Content-Type: application/json" \
    -d '{"prompt":"Hello?","title":"My Chat"}'
- Or canonical route:
  curl -i -X POST https://vscode-internal-16277-beta.beta01.cloud.kavia.ai:3001/api/ask/ \
    -H "Content-Type: application/json" \
    -d '{"prompt":"Hello?","title":"My Chat"}'
- If you receive 502 with "LLM error: OPENAI_API_KEY ...", set OPENAI_API_KEY in the backend .env and restart.
- If curl to :3001 still returns "Cannot POST", a proxy in front of Django is intercepting. Verify your gateway/proxy forwards /api/* to Django, or call Django directly as above.
