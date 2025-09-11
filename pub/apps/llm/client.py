# Minimal Ollama client for local LLM calls.
# Keeps memory use low and returns a plain string.

from django.conf import settings

from .config import SYSTEM_PROMPT
from .utils.context import add_file_context, get_context
from .utils.request import post_prompt

OLLAMA_HOST = settings.OLLAMA_HOST
OLLAMA_MODEL = settings.OLLAMA_MODEL


def generate_answer(
    prompt: str,
    conversation=None,
    file_content: str = None,
) -> str:
    """
    Generates an answer from a local LLM using the Ollama API, optionally
    including conversation history and file content for context.

    Args:
        prompt (str): The user's current query or prompt.
        conversation (optional): The conversation object containing
        previous exchanges (default: None).
        file_content (str, optional): Additional file content to provide
        as context (default: None).

    Returns:
        str: The generated answer from the LLM as a plain string.
    """
    if not prompt:
        return ""

    context = get_context(conversation, file_content) or ""
    full_prompt = SYSTEM_PROMPT

    if context:
        full_prompt += f"\n\nPrevious conversation:\n{context}"

    current_prompt = prompt

    if file_content:
        current_prompt = add_file_context(current_prompt, file_content)

    url = f"{OLLAMA_HOST}/api/generate"

    payload = {
        "model": OLLAMA_MODEL,
        "system": full_prompt,
        "prompt": current_prompt,
        "stream": False,
        "options": {
            "num_ctx": 8192,  # Increased for context
            "temperature": 0.1,
        },
    }

    return post_prompt(prompt, url, payload)
