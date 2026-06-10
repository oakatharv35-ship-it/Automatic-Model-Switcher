# ui.py
import streamlit as st

page_title = "Chat UI"
layout = "centered"

# ---------------------------------------------------------------------------
# Model registry
# ---------------------------------------------------------------------------

# Each entry: (model_id, description)
# Keys follow the convention: {provider}_{tier} for API models,
# {category} or {category}_fast for local models.

MODEL_DESCRIPTIONS: dict[str, tuple[str, str]] = {
    # --- Local: default speed ---
    "coding":                ("qwen3:8b",       "Local model tuned for coding and complex multi-step reasoning."),
    "debugging":             ("deepseek-r1:8b", "Local model specialised in debugging and step-by-step error analysis."),
    "summarization":         ("llama3.1:8b",    "Local model optimised for condensing and summarising content."),
    "structured_output":     ("qwen2.5:7b",     "Local model optimised for structured and formatted output generation."),
    "technical_explanation": ("qwen3:8b",       "Local model tuned for breaking down complex technical concepts."),
    "reasoning":             ("phi4-mini",      "Compact local model tuned for logical reasoning tasks."),
    "general_chat":          ("llama3.1:8b",    "A balanced general-purpose local model for most everyday queries."),
    "fast_simple":           ("gemma4:e4b",     "Lightweight local model for fast, concise 1-2 sentence answers."),

    # --- Local: fast speed ---
    "coding_fast":                ("qwen2.5-coder:3b", "Compact coding-focused local model for quick code-related answers."),
    "debugging_fast":             ("qwen3:4b",         "Compact model for fast debugging and error tracing."),
    "summarization_fast":         ("llama3.2:3b",      "Small, fast local model suited for quick summarisation."),
    "structured_output_fast":     ("qwen2.5:3b",       "Compact model for fast structured output generation."),
    "technical_explanation_fast": ("gemma3:4b",        "Lightweight model for quick technical explanations."),
    "reasoning_fast":             ("qwen3:4b",         "Compact model for fast logical reasoning answers."),
    "general_chat_fast":          ("gemma3:4b",        "Lightweight local model for fast general-purpose answers."),
    "fast_simple_fast":           ("gemma4:e4b",       "Lightest local model for the fastest possible simple answers."),

    # --- OpenAI ---
    "openai_default": ("gpt-5.4-nano", "OpenAI's default model — balanced capability and cost for general use."),
    "openai_cheap":   ("gpt-5-nano",   "OpenAI's cheapest model — fast and affordable for simple tasks."),
    "openai_best":    ("gpt-5.4-mini", "OpenAI's most capable model for complex tasks."),

    # --- Anthropic ---
    "anthropic_default": ("claude-sonnet-4-6",         "Anthropic's default Claude model — strong general-purpose performance."),
    "anthropic_cheap":   ("claude-haiku-4-5-20251001", "Anthropic's lightest Claude model — fast and cost-efficient."),
    "anthropic_best":    ("claude-opus-4-7",           "Anthropic's most powerful Claude model for nuanced, complex tasks."),

    # --- Google ---
    "google_default": ("gemini-3.5-flash",       "Google's default Gemini model — fast and well-rounded."),
    "google_cheap":   ("gemini-3.1-flash-lite",  "Google's cheapest Gemini model — optimised for speed and low cost."),
    "google_best":    ("gemini-3.1-pro-preview", "Google's most capable Gemini model for demanding tasks."),
}

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

STYLES = """
<style>
.stApp {
    background-color: #343541;
    color: white;
}

/* ---- Layout ---- */
.chat-container {
    max-width: 850px;
    margin: auto;
    padding-bottom: 180px;
}

/* ---- Messages ---- */
.user-msg {
    background: #444654;
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 14px;
}

.assistant-msg {
    background: #3a3b47;
    border: 1px solid #565869;
    padding: 16px;
    border-radius: 12px;
    margin-bottom: 14px;
}

.model-tag {
    display: flex;
    align-items: center;
    gap: 4px;
    margin-top: 10px;
    font-size: 11px;
    color: #888;
}

/* ---- Bottom input bar ---- */
.bottom-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 100;
    background: #343541;
    border-top: 1px solid #555;
    padding: 15px 0 20px;
}

.bottom-inner {
    max-width: 850px;
    margin: auto;
}

.small-checkbox {
    margin-top: -8px;
    margin-left: 3px;
}

/* ---- Inputs ---- */
textarea {
    background-color: #40414f !important;
    color: white !important;
    border-radius: 12px !important;
}

.stSelectbox > div > div {
    background-color: #40414f !important;
    color: white !important;
    border-radius: 8px !important;
}

/* ---- Model info expander ---- */
.model-info-expander .streamlit-expanderHeader {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    font-size: 11px !important;
    color: #888 !important;
}
</style>
"""