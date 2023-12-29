from dataclasses import dataclass, field
import json
from src.models import TextModel, CHAT_DEFAULT

@dataclass
class TextTask:
    system_prompt: str
    model: TextModel = field(default_factory=lambda: CHAT_DEFAULT)

    def run(self, user_prompt: str) -> str:
        return self.model.simple_call(self.system_prompt, user_prompt)
    
def parse_chat_gpt_json(hopefully_valid_json_string, max_num_tries = 3):
    try:
        return json.loads(hopefully_valid_json_string, strict = False)
    
    except json.JSONDecodeError as e:
        if max_num_tries == 1:
            raise e
        
        print(f"JSON failed to parse. Using ChatGPT to fix it")
        return parse_chat_gpt_json(
            FIX_JSON.run(
                f"""
                Error: {e}
                JSON: {hopefully_valid_json_string}
                """
            ),
            max_num_tries - 1
        )
    
FIX_JSON = TextTask("""
You are a json expert. Users will give you a python json decoder error
and some json. You job is to fix the json so that the error does not occur again
Return only the fixed json without markdown formatting so that the error does not occur again.
""")