from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Chat, Message


class HealthTests(APITestCase):
    def test_health(self):
        url = reverse('Health')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Server is up!"})


class AskEndpointTests(APITestCase):
    def setUp(self):
        # Ensure demo user is created consistently as views fallback to it
        self.demo_user, _ = User.objects.get_or_create(username="demo")

    @patch("api.services.OpenAIChatService.generate_reply", return_value="Mocked reply")
    def test_ask_creates_new_chat_when_chat_id_absent(self, mock_reply):
        url = reverse('AskQuestion')
        payload = {"prompt": "Hello?", "title": "My Chat"}
        resp = self.client.post(url, data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.data)

        # Response contains chat and answer
        self.assertIn("chat", resp.data)
        self.assertIn("answer", resp.data)
        self.assertEqual(resp.data["answer"], "Mocked reply")

        # Chat created and owned by demo user
        chat_id = resp.data["chat"]["id"]
        chat = Chat.objects.get(pk=chat_id)
        self.assertEqual(chat.owner, self.demo_user)
        self.assertEqual(chat.title, "My Chat")

        # Two messages persisted: user prompt + assistant
        msgs = Message.objects.filter(chat=chat).order_by("created_at", "id")
        self.assertEqual(msgs.count(), 2)
        self.assertEqual(msgs[0].role, "user")
        self.assertEqual(msgs[0].content, "Hello?")
        self.assertEqual(msgs[1].role, "assistant")
        self.assertEqual(msgs[1].content, "Mocked reply")

    @patch("api.services.OpenAIChatService.generate_reply", return_value="Another mocked reply")
    def test_ask_appends_to_existing_chat_when_chat_id_provided(self, mock_reply):
        # Create an existing chat for demo user
        chat = Chat.objects.create(owner=self.demo_user, title="Existing")

        url = reverse('AskQuestion')
        payload = {"chat_id": chat.id, "prompt": "Continue?"}
        resp = self.client.post(url, data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.data)
        self.assertEqual(resp.data["answer"], "Another mocked reply")
        self.assertEqual(resp.data["chat"]["id"], chat.id)

        msgs = Message.objects.filter(chat=chat).order_by("created_at", "id")
        # 2 new messages added in this call (user + assistant)
        self.assertEqual(msgs.count(), 2)
        self.assertEqual(msgs[0].role, "user")
        self.assertEqual(msgs[0].content, "Continue?")
        self.assertEqual(msgs[1].role, "assistant")
        self.assertEqual(msgs[1].content, "Another mocked reply")

    @patch("api.services.OpenAIChatService.generate_reply", return_value="Irrelevant")
    def test_ask_404_when_chat_not_owned_by_user(self, mock_reply):
        # Create another user and chat
        other = User.objects.create_user(username="other")
        other_chat = Chat.objects.create(owner=other, title="Other's chat")

        url = reverse('AskQuestion')
        payload = {"chat_id": other_chat.id, "prompt": "Test?"}
        resp = self.client.post(url, data=payload, format="json")
        # The view uses demo user; since other_chat is not owned by demo, expect 404
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
