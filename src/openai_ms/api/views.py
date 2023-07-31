from typing import Any
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import decorators, generics, status, viewsets, serializers
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Conversation, Prompt
from .serializers import (
    ConversationSerializer,
    ConverseSerializer,
    PromptSerializer,
    StartConversationSerializer,
)
from .services import openai_conversation, openai_prompt


class PromptCreateView(generics.CreateAPIView):
    serializer_class = PromptSerializer

    def create(self, request: Request, *args: str, **kwargs: str) -> Response:
        prompt_text = str(request.data.get("text"))
        if not prompt_text:
            raise ValueError("Text not provided")
        prompt = Prompt(text=prompt_text)
        response = openai_prompt(prompt)
        prompt.response = response
        prompt.save()
        serializer = self.get_serializer(prompt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PromptListView(generics.ListAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer


class PromptUpdateView(generics.UpdateAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    lookup_field = "id"

    def update(self, request: Request, *args: str, **kwargs: str) -> Response:
        prompt_id = int(kwargs["id"])
        prompt_text = str(request.data.get("text"))
        if not prompt_text:
            raise ValueError("Text not provided")
        prompt = Prompt.objects.get(pk=prompt_id)
        prompt.text = prompt_text
        response = openai_prompt(prompt)
        prompt.response = response
        prompt.save()
        serializer = self.get_serializer(prompt)
        return Response(serializer.data)


class PromptDeleteView(generics.DestroyAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    lookup_field = "id"


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer

    def get_serializer_class(self) -> type[serializers.BaseSerializer[Any]]:
        if self.action == "start":
            return StartConversationSerializer
        elif self.action == "converse":
            return ConverseSerializer
        return super().get_serializer_class()

    @swagger_auto_schema(
        operation_description="Create new conversation",
        responses={
            201: openapi.Response("Conversation started", ConversationSerializer)
        },
    )
    @decorators.action(detail=False, methods=["post"])
    def start(self, request: Request, *args: str, **kwargs: str) -> Response:
        prompt_text = str(request.data.get("text"))
        if not prompt_text:
            raise ValueError("Text not provided")
        conversation = Conversation.objects.create(name=prompt_text)
        prompt = Prompt(text=prompt_text, conversation=conversation)
        response = openai_prompt(prompt)
        prompt.response = response
        prompt.save()
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Continue conversation",
        responses={200: openapi.Response("Conversed", ConversationSerializer)},
    )
    @decorators.action(detail=True, methods=["put"])
    def converse(self, request: Request, *args: str, **kwargs: str) -> Response:
        prompt_text = str(request.data.get("text"))
        conversation_id = int(request.data.get("conversation_id"))
        if not prompt_text or not conversation_id:
            raise ValueError("Conversation or Text not provided")

        conversation = Conversation.objects.get(pk=conversation_id)
        prompts = list(conversation.prompts.all())
        prompt = Prompt(text=prompt_text, conversation=conversation)
        prompts.append(prompt)
        response = openai_conversation(prompts)
        prompt.response = response
        prompt.save()
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)
