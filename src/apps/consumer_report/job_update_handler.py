from typing import Any, Callable
import streamlit as st


def job_update_handler(name: str, old_value: Any, new_value: Any): 
    if name not in job_update_handlers.keys():
        return
    job_update_handlers[name](old_value, new_value)

def current_task_updated(_, current_task: str):
    st.write(f'Started New Task: {current_task}')

job_update_handlers: dict[str, Callable[[Any, Any], None]] = {
    'current_task': current_task_updated
}