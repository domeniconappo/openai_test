import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from openai_ms.api.models import Prompt

pytestmark = pytest.mark.django_db


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


def test_create_prompt(
    api_client: APIClient, create_prompt_data: dict, response_prompt_data: dict
) -> None:
    create_url = reverse("prompt-create")
    response = api_client.post(create_url, create_prompt_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Prompt.objects.count() == 1
    assert response.data["text"] == response_prompt_data["text"]
    assert response.data["response"] == response_prompt_data["response"]


def test_list_prompts(api_client: APIClient, existing_prompt: Prompt) -> None:
    list_url = reverse("prompt-list")
    response = api_client.get(list_url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


def test_update_prompt(api_client: APIClient, existing_prompt: Prompt) -> None:
    update_data = {"text": "Updated Prompt Text"}
    update_response = {
        "text": "Updated Prompt Text",
        "response": "Updated Response Text",
    }
    update_url = reverse("prompt-update", kwargs={"id": existing_prompt.id})
    response = api_client.put(update_url, update_data)
    assert response.status_code == status.HTTP_200_OK
    existing_prompt.refresh_from_db()
    assert existing_prompt.text == update_response["text"]
    assert existing_prompt.response == update_response["text"]


def test_delete_prompt(api_client: APIClient, existing_prompt: Prompt) -> None:
    delete_url = reverse("prompt-delete", kwargs={"id": existing_prompt.id})
    response = api_client.delete(delete_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Prompt.objects.count() == 0
