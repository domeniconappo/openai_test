import pytest

from openai_ms.api.models import Prompt
from openai_ms.api.serializers import PromptSerializer

pytestmark = pytest.mark.django_db


@pytest.fixture
def create_prompt_data() -> dict:
    return {"text": "Test Prompt Text"}


@pytest.fixture
def existing_prompt() -> Prompt:
    return Prompt.objects.create(text="Existing Prompt Text", response="Response Text")


def test_prompt_serializer(create_prompt_data: dict) -> None:
    serializer = PromptSerializer(data=create_prompt_data)
    assert serializer.is_valid()
    prompt = serializer.save()
    assert isinstance(prompt, Prompt)
    assert prompt.text == create_prompt_data["text"]
    assert prompt.response == create_prompt_data["response"]
