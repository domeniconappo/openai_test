from typing import Any
import openai

from .models import Prompt


def openai_prompt(prompt: Prompt) -> Any:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt.text}]
    )
    res_text = response.choices[0].message.content
    return res_text
