# Q&A Backend Runbook

Steps to install and start locally:

1) Install dependencies
   pip install -r requirements.txt

2) Setup environment
   cp .env.example .env
   # Edit .env to set DJANGO_SECRET_KEY and, if you plan to call /api/ask, set OPENAI_API_KEY.

3) Apply migrations
   python manage.py migrate

4) Start server
   python manage.py runserver 0.0.0.0:8000

Health check:
- GET http://localhost:8000/api/health/ should return:
  {"message":"Server is up!"}

API Docs:
- Swagger UI: http://localhost:8000/docs/
- Redoc: http://localhost:8000/redoc/
