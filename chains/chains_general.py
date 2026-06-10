from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


def default_chain(chain_input, model, prompt) -> str:
    llm = ChatOllama(model=model, temperature=0.7)
    chain = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("user", "{input}")
    ]) | llm    
    
    response = chain.invoke(input=chain_input)
    return response.content.strip()

def specialized_chain(chain_input, model, prompt) -> str:
    llm = ChatOllama(model=model, temperature=0.7)
    chain = ChatPromptTemplate.from_messages([
        ("system", prompt),
        ("user", "{input}")
    ]) | llm

    response = chain.invoke(input=chain_input)
    return response.content.strip()