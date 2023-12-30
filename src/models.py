from dataclasses import dataclass, field
from openai import OpenAI, OpenAIError

def safe_init_open_ai():
    try:
        return OpenAI()
    except OpenAIError:
        # This happens when deployed to streamlit cloud as no api key will be set
        # but users set their own before they can call and models so it is okay
        return None

@dataclass
class Model():
    tag: str
    client: OpenAI | None = safe_init_open_ai()

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