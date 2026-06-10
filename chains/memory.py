from typing import Dict, List
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from registry.model_registry import select_other_model
from registry.prompts import SUMMARIZER_PROMPT
from backend.history import create_prompt_format, add_message_to_memory


def summarize_history(history: list) -> str:
    conversation = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])

    conversation_history = create_prompt_format(conversation)
    llm = ChatOllama(model=select_other_model("history"), temperature=0.7)
    chain = ChatPromptTemplate.from_messages([
        ("system", SUMMARIZER_PROMPT),
    ]) | llm

    summary = chain.invoke({"conversation_history": conversation_history})
    return summary.content.strip()