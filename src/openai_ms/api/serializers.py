from rest_framework import serializers

from .models import Conversation, Prompt


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ("text", "response")


class ConversationSerializer(serializers.Serializer):
    prompts = PromptSerializer(many=True)


class StartConversationSerializer(serializers.Serializer):
    text = serializers.CharField()


class ConverseSerializer(serializers.Serializer):
    conversation_id = serializers.IntegerField()
    text = serializers.CharField()
