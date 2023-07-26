from django.db import models
from django.utils import timezone



class Prompt(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    text = models.TextField(null=False)
    response = models.TextField(null=True)

    def __str__(self) -> str:
        return f"Prompt #{self.id}: {self.text} - {self.response}"
