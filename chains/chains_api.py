from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from registry.model_registry import MODEL_REGISTRY_OPENAI, MODEL_REGISTRY_ANTHROPIC, MODEL_REGISTRY_GOOGLE


def get_models(provider: str, category: str, api_key: str):
    providers = {
        "OpenAI": ChatOpenAI(
            model=MODEL_REGISTRY_OPENAI.get(category, MODEL_REGISTRY_OPENAI["default"]),
            api_key=api_key,
            temperature=0.7,
        ),
        "Anthropic": ChatAnthropic(
            model=MODEL_REGISTRY_ANTHROPIC.get(category, MODEL_REGISTRY_ANTHROPIC["default"]),
            api_key=api_key,
            temperature=0.7,
        ),
        "Google": ChatGoogleGenerativeAI(
            model=MODEL_REGISTRY_GOOGLE.get(category, MODEL_REGISTRY_GOOGLE["default"]),
            google_api_key=api_key,
            temperature=0.7,
        )
    }
    return providers.get(provider)

def handle_output(response) -> str:
    try: 
        return response.content.strip()
    except:
        return " ".join(
            block['text'] for block in content
            if isinstance(block, dict) and "text" in block
        ).strip()

def run_api_chains(chain_input, choices: list, prompt: str) -> str:
    llm = get_models(choices[0], choices[1], choices[2])
    print(llm)
    chain = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("user", "{input}")
    ]) | llm
    response = chain.invoke(input=chain_input)
    content = response.content
    print(content)

    return handle_output(response)

def openai_chain(user_input: str, category: str, api_key: str) -> str:
    llm = get_models("openai", category, api_key)
    chain = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "{input}")
    ]) | llm

    response = chain.invoke(input=user_input)
    return response.content.strip()

def anthropic_chain(user_input: str, category: str, api_key: str) -> str:
    llm = get_models("anthropic", category, api_key)
    chain = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "{input}")
    ]) | llm

    response = chain.invoke(input=user_input)
    return response.content.strip()

def google_chain(user_input: str, category: str, api_key: str) -> str:
    llm = get_models("google", category, api_key)
    chain = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "{input}")
    ]) | llm

    response = chain.invoke(input=user_input)
    content = response.content

    # Handle list content (Gemini returns a list of dicts with 'text' keys)
    if isinstance(content, list):
        return " ".join(
            block["text"] for block in content
            if isinstance(block, dict) and "text" in block
        ).strip()

    # Handle plain string content
    return content.strip()