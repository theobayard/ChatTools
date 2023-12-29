from dataclasses import dataclass
from openai import OpenAI

@dataclass
class Model():
    tag: str
    client = OpenAI()

@dataclass
class TextModel(Model):
    token_limit: int

    def simple_call(self, system_prompt: str, user_prompt: str) -> str | None:
        return self.client.chat.completions.create(
            model=self.tag,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        ).choices[0].message.content

CHAT_GPT_4_TURBO_PREVIEW = TextModel('gpt-4-1106-preview', 	128000)
CHAT_DEFAULT = CHAT_GPT_4_TURBO_PREVIEW