from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from registry.model_registry import select_other_model
import base64


def encode_uploaded_image(uploaded_file) -> tuple[str, str]:
    """Encode a Streamlit UploadedFile to (base64_string, mime_type)."""
    mime_type = uploaded_file.type or "image/jpeg"
    image_b64 = base64.b64encode(uploaded_file.read()).decode("utf-8")
    return image_b64, mime_type


def multimodal_chain(chain_input: dict, model_name: str, prompt: str) -> str:
    """
    Run a multimodal vision chain.

    Expects chain_input keys:
        image_b64  (str)  — base64-encoded image
        mime_type  (str)  — e.g. 'image/jpeg'
        input      (str)  — user text prompt (may be a default fallback)
        recap      (str)  — optional history summary, present only if memory=True
    """
    # ── Build system message, injecting memory recap if present ──
    system_content = prompt
    if recap := chain_input.get("recap"):
        system_content += f"\n\nConversation so far:\n{recap}"

    # ── Build multimodal user message ────────────────────────────
    image_url = f"data:{chain_input['mime_type']};base64,{chain_input['image_b64']}"
    content = [
        {
            "type": "image_url",
            "image_url": {"url": image_url},
        },
        {
            "type": "text",
            "text": chain_input["input"],
        },
    ]

    messages = [
        SystemMessage(content=system_content),
        HumanMessage(content=content),
    ]

    llm = ChatOllama(model=model_name, temperature=0.7)
    response = llm.invoke(messages)

    return response.content.strip()