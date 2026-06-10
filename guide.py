from chains.chains_general import default_chain, specialized_chain
from chains.chains_api import run_api_chains
from chains.chains_backend import classifier_chain, summarize_history

from backend.search import search_web
from registry.model_registry import select_default_model, select_fast_model
from registry.prompts import (
    GENERAL_PROMPT, GENERAL_WITH_MEMORY_PROMPT,
    SEARCH_GENERAL_PROMPT, MEMORY_SEARCH_GENERAL_PROMPT,
    CATEGORIZED_PROMPT, CATEGORIZED_WITH_MEMORY_PROMPT,
    SEARCH_CATEGORIZED_PROMPT, MEMORY_SEARCH_CATEGORIZED_PROMPT,
    API_STANDARD_PROMPT, API_MEMORY_PROMPT,
    API_SEARCH_PROMPT, API_FULL_PROMPT,
    CATEGORY_NAMES, CATEGORY_DESCRIPTIONS,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _gather_context(
    user_messages: str,
    history: list,
    use_classifier: bool = False,
    use_search: bool = False,
    use_memory: bool = False,
) -> tuple[str, list, str]:
    """Fetch model category, search results, and history summary as needed."""
    model_info = classifier_chain(user_messages) if use_classifier else ""
    search_info = search_web(user_messages) if use_search else []

    if use_memory:
        print("Summarizing history for memory...")
        history_summary = summarize_history(history)
    else:
        history_summary = ""

    return model_info, search_info, history_summary


def _with_sources(response: str, search_info: list) -> str:
    """Append source links to a response when search was used."""
    sources = "<br>".join(search_info[1])
    return f"{response}<br><br><br><br>Sources Found: <br>{sources}"


def _select_prompt(use_memory: bool, use_search: bool, general: bool) -> str:
    """Pick the right prompt template based on active flags."""
    prompts = {
        (False, False): GENERAL_PROMPT          if general else CATEGORIZED_PROMPT,
        (True,  False): GENERAL_WITH_MEMORY_PROMPT if general else CATEGORIZED_WITH_MEMORY_PROMPT,
        (False, True):  SEARCH_GENERAL_PROMPT   if general else SEARCH_CATEGORIZED_PROMPT,
        (True,  True):  MEMORY_SEARCH_GENERAL_PROMPT if general else MEMORY_SEARCH_CATEGORIZED_PROMPT,
    }
    return prompts[(use_memory, use_search)]


def _api_prompt(use_memory: bool, use_search: bool) -> str:
    prompts = {
        (False, False): API_STANDARD_PROMPT,
        (True,  False): API_MEMORY_PROMPT,
        (False, True):  API_SEARCH_PROMPT,
        (True,  True):  API_FULL_PROMPT,
    }
    return prompts[(use_memory, use_search)]


# ---------------------------------------------------------------------------
# Local model routing
# ---------------------------------------------------------------------------

def respond_user_using_local_model(
    user_input: str,
    history: list,
    choices: list,
    user_messages: str,
) -> tuple[str, str]:
    use_classifier, use_fast, use_memory, use_search = choices

    model_info, search_info, history_summary = _gather_context(
        user_messages, history,
        use_classifier=use_classifier,
        use_search=use_search,
        use_memory=use_memory,
    )

    # A "fast_simple" classifier result overrides the speed flag
    if model_info == "fast_simple":
        use_fast = True

    is_specialized = use_classifier and model_info in CATEGORY_NAMES
    category = model_info if is_specialized else "general_chat"
    tag = category + ("_fast" if use_fast else "")

    model = (select_fast_model if use_fast else select_default_model)(category)

    query = user_input
    if use_fast:
        query += "\nAnswer very briefly and simply, in 1-2 sentences."

    chain_input: dict = {"input": query}
    if is_specialized:
        chain_input["category"] = category
        chain_input["category_description"] = CATEGORY_DESCRIPTIONS.get(category)
    if use_memory:
        chain_input["recap"] = history_summary
    if use_search:
        chain_input["context"] = search_info[0]

    prompt = _select_prompt(use_memory, use_search, general=not is_specialized)
    run = specialized_chain if is_specialized else default_chain
    response = run(chain_input, model, prompt)

    if use_search:
        response = _with_sources(response, search_info)

    return response, tag


# ---------------------------------------------------------------------------
# API model routing
# ---------------------------------------------------------------------------

def respond_user_using_api(
    user_input: str,
    history: list,
    choices: list,
    user_messages: str,
) -> str:
    provider_choices = choices[:3]   # provider, model, extra provider options
    use_fast, use_memory, use_search = choices[-3:]

    _, search_info, history_summary = _gather_context(
        user_messages, history,
        use_search=use_search,
        use_memory=use_memory,
    )

    print(f"Provider: {choices[0]} - {choices[1]}")
    print(f"Search Info: {search_info}")
    print(f"History Summary: {history_summary}")

    query = user_input
    if use_fast:
        query += "\nAnswer very briefly and simply, in 1-2 sentences."

    chain_input: dict = {"input": query}
    if use_memory:
        chain_input["conversation_summary"] = history_summary
    if use_search:
        chain_input["search_results"] = search_info[0]

    prompt = _api_prompt(use_memory, use_search)
    response = run_api_chains(chain_input, provider_choices, prompt)

    if use_search:
        response = _with_sources(response, search_info)

    return response