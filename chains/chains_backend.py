from typing import Dict, List
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from registry.model_registry import select_other_model
from registry.prompts import CLASSIFIER_PROMPT, SUMMARIZER_PROMPT, categories_formatted
from backend.history import create_prompt_format, add_message_to_memory


def summarize_history(history: list) -> str:
    conversation = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
    print(conversation)

    llm = ChatOllama(model=select_other_model("history"), temperature=0.1)
    chain = ChatPromptTemplate.from_messages([
        ("system", SUMMARIZER_PROMPT),
        ("user", "Summarize this conversation:\n\n{conversation_history}\n\nSummary:")
    ]) | llm

    summary = chain.invoke({"conversation_history": conversation})
    return summary.content.strip()


def classifier_chain(user_input: str) -> str:
    classifier_llm = ChatOllama(model=select_other_model("classification"), temperature=0.0)

    chain = ChatPromptTemplate.from_messages([
        ("system", CLASSIFIER_PROMPT),
        ("user", "Message: {input}\n\nCategory: ")
    ]) | classifier_llm

    response = chain.invoke({
        "input": user_input, 
        "categories": categories_formatted
        })
    return response.content.strip()