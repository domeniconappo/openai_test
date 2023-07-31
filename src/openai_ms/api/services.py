from typing import Any

import openai

from .models import Prompt


def openai_prompt(prompt: Prompt) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt.text}]
    )
    res_text = response.choices[0].message.content
    return str(res_text)


def openai_conversation(prompts: list[Prompt]) -> str:
    messages = []
    # Convert prompt objects into a conversation for ChatCompletion API
    for prompt in prompts:
        messages.append({"role": "user", "content": prompt.text})
        if prompt.response:
            messages.append({"role": "assistant", "content": prompt.response})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    res_text = response.choices[0].message.content
    return str(res_text)
