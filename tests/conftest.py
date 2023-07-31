import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from openai_ms.api import views
from openai_ms.api.models import Prompt, Conversation


@pytest.fixture
def mock_openai(monkeypatch: pytest.MonkeyPatch) -> None:
    def mock_return(prompt: Prompt) -> str:
        return "Response Test Prompt Text"

    monkeypatch.setattr(views, "openai_prompt", mock_return)
    monkeypatch.setattr(views, "openai_conversation", mock_return)


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def create_prompt_data() -> dict:
    return {"text": "Test Prompt Text"}


@pytest.fixture
def response_prompt_data() -> dict:
    return {"text": "Test Prompt Text", "response": "Response Test Prompt Text"}


@pytest.fixture
def existing_prompt() -> Prompt:
    return Prompt.objects.create(
        text="Existing Prompt Text", response="Existing Response Text"
    )


@pytest.fixture
def existing_conversation() -> Conversation:
    conversation = Conversation.objects.create(name="Test Conversation")
    Prompt.objects.create(
        text="Existing Prompt Text 1", response="Existing Response Text 1", conversation=conversation
    )
    Prompt.objects.create(
        text="Existing Prompt Text 2", response="Existing Response Text 2", conversation=conversation
    )
    Prompt.objects.create(
        text="Existing Prompt Text 3", response="Existing Response Text 3", conversation=conversation
    )
    return conversation
