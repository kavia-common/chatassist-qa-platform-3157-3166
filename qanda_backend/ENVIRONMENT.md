# Backend Environment and Frontend Alignment

This backend reads configuration from environment variables (via python-dotenv). Use `.env` for local dev (copy from `.env.example`), and set environment variables in your deployment environment.

Backend-only secrets (never in frontend):
- OPENAI_API_KEY: Required to generate answers in /api/ask. This must never be exposed to a browser.

Public/shared configuration (safe to mirror in frontend):
- PUBLIC_BACKEND_BASE_URL: Public base URL of this backend (e.g., http://localhost:8000 or https://your-domain.com).
  - Frontend should construct its API base as: `${PUBLIC_BACKEND_BASE_URL}/api`
  - Example frontend env: REACT_APP_API_BASE_URL=${PUBLIC_BACKEND_BASE_URL}/api
- CORS_ALLOWED_ORIGINS: Comma-separated list of allowed frontend origins (e.g., http://localhost:3000).
  - Include your frontend origin(s) to allow browser requests.

Other backend config:
- OPENAI_MODEL: Optional model name (defaults to `gpt-4o-mini`)
- DJANGO_SECRET_KEY, DEBUG, ALLOWED_HOSTS, TIME_ZONE
- DB_* for database overrides (defaults to SQLite)

CORS behavior:
- If `CORS_ALLOWED_ORIGINS` is provided, CORS is restricted to those origins.
- If not provided, CORS is open for convenience in local development (not recommended for production).

Proxy/Ingress:
- The backend respects `USE_X_FORWARDED_HOST` and `SECURE_PROXY_SSL_HEADER` to build correct docs URLs behind proxies.
- Adjust these only if your deployment requires it.

Usage:
1) cp .env.example .env
2) Set OPENAI_API_KEY (backend-only).
3) Set PUBLIC_BACKEND_BASE_URL (public URL of backend).
4) Set CORS_ALLOWED_ORIGINS to include your frontend URL (e.g., http://localhost:3000).
5) Start the server.

Frontend alignment:
- Ensure frontend sets REACT_APP_API_BASE_URL to `${PUBLIC_BACKEND_BASE_URL}/api`.
- Never place OPENAI_API_KEY in the frontend.
