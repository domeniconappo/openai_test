import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from openai_ms.api import views
from openai_ms.api.models import Conversation, Prompt

pytestmark = pytest.mark.django_db


def test_create_conversation(
    api_client: APIClient,
    create_prompt_data: dict,
    mock_openai: None,
) -> None:
    create_url = reverse("conversation")
    response = api_client.post(create_url, create_prompt_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Prompt.objects.count() == 1
    assert Conversation.objects.count() == 1
    prompt = Prompt.objects.first()
    conversation = Conversation.objects.first()
    assert prompt.conversation == conversation
    assert conversation.name == create_prompt_data["text"]
    assert list(conversation.prompts.all()) == [prompt]


def test_converse(
    api_client: APIClient,
    create_prompt_data: dict,
    existing_conversation: Conversation,
    mock_openai: None,
) -> None:
    create_url = reverse("conversation")
    create_prompt_data["conversation_id"] = existing_conversation.id
    response = api_client.put(create_url, create_prompt_data)
    assert response.status_code == status.HTTP_200_OK
    assert existing_conversation.prompts.count() == 4
