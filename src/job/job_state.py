from dataclasses import dataclass, field
from typing import Any, Callable
from openai import OpenAI


from ..models import CHAT_DEFAULT, TextModel

@dataclass
class JobState:
    user_prompt: str
    current_task: str | None = None
    text_model: TextModel = field(default_factory = lambda: CHAT_DEFAULT)
    # Called with (field_name, old_value, new_value) when state changes
    on_update: Callable[[str, Any, Any], None] | None = None

    def __setattr__(self, __name: str, __value: Any) -> None:
        """
        Allows interface to provide live updates via callback
        """
        if self.on_update:
            if __name in self.__dict__.keys():
                self.on_update(__name, self.__dict__[__name], __value)
            else:
                self.on_update(__name, None, __value)

        self.__dict__[__name] = __value
        

