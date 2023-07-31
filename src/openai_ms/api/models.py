from django.db import models
from django.utils import timezone


class Prompt(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    conversation = models.ForeignKey(
        "Conversation", related_name="prompts", on_delete=models.CASCADE, null=True,
    )
    text = models.TextField(null=False)
    response = models.TextField(null=True)

    def __str__(self) -> str:
        return f"Prompt #{self.id}: {self.text} - {self.response}"


class Conversation(models.Model):
    name = models.TextField(null=False)
    def __str__(self) -> str:
        return f"Conversation #{self.id}"
