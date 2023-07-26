from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request

from .models import Prompt
from .serializers import PromptSerializer
from .services import openai_prompt


class PromptCreateView(generics.CreateAPIView):
    serializer_class = PromptSerializer

    def create(self, request: Request, *args: str, **kwargs: str) -> Response:
        prompt_text = str(request.data.get("text"))
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
        prompt_id = int(kwargs.get("id"))
        prompt_text = str(request.data.get("text"))
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
