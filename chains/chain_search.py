from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from registry.model_registry import select_default_model, select_other_model, select_fast_model
from registry.prompts import *
from backend.history import create_prompt_format, add_message_to_memory
from backend.search import search_web


primary_llm = ChatOllama(model=select_default_model("general_chat"), temperature=0.7)
classifier_llm = ChatOllama(model=select_other_model("classification"), temperature=0.0)


def classifier_chain(user_input: str) -> str:
    
    chain = ChatPromptTemplate.from_messages([
        ("system", CLASSIFIER_PROMPT),
        ("user", "Message: {input}\n\nCategory: ")
    ]) | classifier_llm

    response = chain.invoke({
        "input": user_input, 
        "categories": categories_formatted
        })
    return response.content.strip()


def first_general_chain_search(user_input: str, context: str) -> str:
    print("Search context:", context)
    primary_llm = ChatOllama(model=select_default_model("general_chat"), temperature=0.7)
    print("Running first_general_chain_search")
    # formatted_prompt = prompt.format_messages(input=user_input, history=history)
    chain = ChatPromptTemplate.from_messages([
        ("system", SEARCH_GENERAL_PROMPT),
        ("user", "{input}")
    ]) | primary_llm    
    
    response = chain.invoke({"input": user_input, "context": context})
    return response.content.strip()
    

def categorized_chain_search(user_input: str, context: str) -> str:
    print("Search context:", context)
    print("Running categorized_chain_search")
    category = classifier_chain(user_input)
    print(category)
    try:
        llm = ChatOllama(model=select_default_model(category), temperature=0.7)
    except:
        llm = ChatOllama(model=select_default_model("general_chat"), temperature=0.7)

    chain = ChatPromptTemplate.from_messages([
            ("system", SEARCH_CATEGORIZED_PROMPT),
            ("user", "{input}")
    ]) | llm

    response = chain.invoke({
        "input": user_input,
        "category": category, 
        "category_description": CATEGORY_DESCRIPTIONS.get(category),
        "context": context
    })
    return response.content.strip()
    

def general_chain_with_memory_search(user_input: str, history: str, context: str) -> str:
    print("Search context:", context)
    primary_llm = ChatOllama(model=select_default_model("general_chat"), temperature=0.7)
    print("Running general_chain_with_memory_search")
    chain = ChatPromptTemplate.from_messages([
        ("system", MEMORY_SEARCH_GENERAL_PROMPT),
        ("user", "{input}")
    ]) | primary_llm

    response = chain.invoke({
        "input": user_input,
        "recap": history,
        "context": context
    })

    return response.content.strip()


def categorized_chain_with_memory_search(user_input: str, history: str, context: str) -> str:
    print("Search context:", context)
    print("Running categorized_chain_with_memory_search")
    category = classifier_chain(user_input)
    print(category)
    try:
        llm = ChatOllama(model=select_default_model(category), temperature=0.7)
    except:
        llm = ChatOllama(model=select_default_model("general_chat"), temperature=0.7)

    chain = ChatPromptTemplate.from_messages([
        ("system", MEMORY_SEARCH_CATEGORIZED_PROMPT),
        ("user", "{input}")
    ]) | llm

    response = chain.invoke({
        "input": user_input, 
        "recap": history, 
        "category": category, 
        "context": context,
        "category_description": CATEGORY_DESCRIPTIONS.get(category)
    })
    return response.content.strip()


def first_general_chain_search_fast(user_input: str, context: str) -> str:
    print("Search context:", context)
    primary_llm = ChatOllama(model=select_fast_model("general_chat"), temperature=0.7)
    print("Running first_general_chain_search_fast")
    # formatted_prompt = prompt.format_messages(input=user_input, history=history)
    chain = ChatPromptTemplate.from_messages([
        ("system", SEARCH_GENERAL_PROMPT),
        ("user", "{input}" + "\nAnswer very briefly and simply, in 1-2 sentences.")
    ]) | primary_llm    
    
    response = chain.invoke({"input": user_input, "context": context})
    return response.content.strip()
    

def categorized_chain_search_fast(user_input: str, context: str) -> str:
    print("Search context:", context)
    print("Running categorized_chain_search_fast")
    category = classifier_chain(user_input)
    print(category)
    try:
        llm = ChatOllama(model=select_fast_model(category), temperature=0.7)
    except:
        llm = ChatOllama(model=select_fast_model("general_chat"), temperature=0.7)

    chain = ChatPromptTemplate.from_messages([
            ("system", SEARCH_CATEGORIZED_PROMPT),
            ("user", "{input}" + "\nAnswer very briefly and simply, in 1-2 sentences.")
    ]) | llm

    response = chain.invoke({
        "input": user_input,
        "category": category, 
        "category_description": CATEGORY_DESCRIPTIONS.get(category),
        "context": context
    })
    return response.content.strip()
    

def general_chain_with_memory_search_fast(user_input: str, history: str, context: str) -> str:
    print("Search context:", context)
    primary_llm = ChatOllama(model=select_fast_model("general_chat"), temperature=0.7)
    print("Running general_chain_with_memory_search_fast")
    chain = ChatPromptTemplate.from_messages([
        ("system", MEMORY_SEARCH_GENERAL_PROMPT),
        ("user", "{input}" + "\nAnswer very briefly and simply, in 1-2 sentences.")
    ]) | primary_llm

    response = chain.invoke({
        "input": user_input,
        "recap": history,
        "context": context
    })

    return response.content.strip()


def categorized_chain_with_memory_search_fast(user_input: str, history: str, context: str) -> str:
    print("Search context:", context)
    print("Running categorized_chain_with_memory_search_fast")
    category = classifier_chain(user_input)
    print(category)
    try:
        llm = ChatOllama(model=select_fast_model(category), temperature=0.7)
    except:
        llm = ChatOllama(model=select_fast_model("general_chat"), temperature=0.7)

    chain = ChatPromptTemplate.from_messages([
        ("system", MEMORY_SEARCH_CATEGORIZED_PROMPT),
        ("user", "{input}" + "\nAnswer very briefly and simply, in 1-2 sentences.")
    ]) | llm

    response = chain.invoke({
        "input": user_input, 
        "recap": history, 
        "category": category, 
        "context": context,
        "category_description": CATEGORY_DESCRIPTIONS.get(category)
    })
    return response.content.strip()