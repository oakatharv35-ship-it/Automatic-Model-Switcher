from typing import Dict, List
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from registry.model_registry import select_other_model
from registry.prompts import SUMMARIZER_PROMPT


def add_message_to_memory(history: list, role: str, content: str) -> list:
    history.append({"role": role, "content": content})
    return history

def create_prompt_format(conversation: str) -> str:
    return f"""Summarize the following conversation:

CONVERSATION START
{conversation}
CONVERSATION END

Summary:"""
