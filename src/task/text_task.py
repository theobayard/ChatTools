import json
from ..models import CHAT_DEFAULT

    
def parse_chat_gpt_json(hopefully_valid_json_string, model = CHAT_DEFAULT, max_num_tries = 3):
    try:
        return json.loads(hopefully_valid_json_string, strict = False)
    
    except json.JSONDecodeError as e:
        if max_num_tries == 1:
            raise e
        
        print(f"JSON failed to parse. Using ChatGPT to fix it")
        return parse_chat_gpt_json(
            model.simple_call(FIX_JSON,
                f"""
                Error: {e}
                JSON: {hopefully_valid_json_string}
                """
            ),
            model = model,
            max_num_tries = max_num_tries - 1
        )
    
FIX_JSON = """
You are a json expert. Users will give you a python json decoder error
and some json. You job is to fix the json so that the error does not occur again
Return only the fixed json without markdown formatting so that the error does not occur again.
"""