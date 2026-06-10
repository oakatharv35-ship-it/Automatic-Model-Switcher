DEFAULT_MODEL_REGISTRY = {
    "coding": "qwen3:8b",
    "debugging": "deepseek-r1:8b",
    "summarization": "llama3.1:8b",
    "structured_output": "qwen2.5:7b",
    "technical_explanation": "qwen3:8b",
    "reasoning": "phi4-mini",
    "general_chat": "llama3.1:8b",
    "fast_simple": "gemma4:e4b",
    "image": "llama3.2-vision:11b"
}

OTHER_MODEL_REGISTRY = {

    "classification": "qwen2.5:0.5b",
    "history": "qwen2.5:0.5b"
}

FAST_MODEL_REGISTRY = {
    "coding": "qwen2.5-coder:3b",
    "debugging": "qwen3:4b",
    "summarization": "llama3.2:3b",
    "structured_output": "qwen2.5:3b",
    "technical_explanation": "gemma3:4b",
    "reasoning": "qwen3:4b",
    "general_chat": "gemma3:4b",
    "fast_simple": "gemma4:e4b",
    "image": "llama3.2-vision:11b"
}

MODEL_REGISTRY_OPENAI = {
    "default": "gpt-5.4-nano",
    "cheap": "gpt-5-nano",
#    "coding": "gpt-5.3-codex",
    "best": "gpt-5.4-mini"
}

MODEL_REGISTRY_ANTHROPIC = {
    "best": "claude-opus-4-7",
    "default": "claude-sonnet-4-6",
    "cheap": "claude-haiku-4-5-20251001"
}

MODEL_REGISTRY_GOOGLE = {
    "best": "gemini-3.1-pro-preview",
    "default": "gemini-3.5-flash",
    "cheap": "gemini-3.1-flash-lite"
}


def select_default_model(route: str) -> str:
    return DEFAULT_MODEL_REGISTRY.get(route)

def select_other_model(route: str) -> str:
    return OTHER_MODEL_REGISTRY.get(route)

def select_fast_model(route: str) -> str:
    return FAST_MODEL_REGISTRY.get(route)