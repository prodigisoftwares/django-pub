# Minimal Ollama client for local LLM calls.
# Keeps memory use low and returns a plain string.

from django.conf import settings

from .config import SYSTEM_PROMPT
from .utils.context import add_file_context, append_context_parts
from .utils.request import post_prompt

OLLAMA_HOST = settings.OLLAMA_HOST
OLLAMA_MODEL = settings.OLLAMA_MODEL


def generate_answer(
    prompt: str,
    conversation=None,
    file_content: str = None,
) -> str:
    if not prompt:
        return ""

    context = ""

    if conversation:
        previous_exchanges: list = (
            conversation.exchanges.select_related()
            .prefetch_related("attachments")
            .order_by("created_at")[:10]
        )

        if previous_exchanges.exists():
            context_parts = []

            for exchange in previous_exchanges:
                context_parts = append_context_parts(
                    context_parts, exchange, file_content
                )

            context = "\n\n".join(context_parts) + "\n\n"

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
