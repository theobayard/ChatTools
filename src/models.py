from dataclasses import dataclass
from openai import OpenAI

@dataclass
class Model():
    tag: str
    client: OpenAI = OpenAI()

@dataclass
class TextModel(Model):
    token_limit: int = 8128

    def simple_call(self, system_prompt: str, user_prompt: str) -> str:
        content = self.client.chat.completions.create(
            model=self.tag,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        ).choices[0].message.content

        if content is None:
            raise Exception("Prompt returned no content")
        
        return content

CHAT_GPT_4_TURBO_PREVIEW = TextModel('gpt-4-1106-preview', 	token_limit=128000)
CHAT_DEFAULT = CHAT_GPT_4_TURBO_PREVIEW