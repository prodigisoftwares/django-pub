# Minimal Ollama client for local LLM calls.
# Keeps memory use low and returns a plain string.

import requests
from django.conf import settings

from .config import SYSTEM_PROMPT

OLLAMA_HOST = settings.OLLAMA_HOST
OLLAMA_MODEL = settings.OLLAMA_MODEL
TIMEOUT = settings.OLLAMA_TIMEOUT


def _append_context_parts(
    context_parts: list[str], exchange, file_content: str | None
) -> list[str]:
    context_parts.append(f"User: {exchange.query}")

    if not file_content:
        attachments = exchange.attachments.all()

        if attachments:
            for attachment in attachments:
                context_parts.append(f"[Attached file: {attachment.filename}]")

                content = attachment.content

                if len(content) > 3000:  # pragma: no cover
                    content = content[:3000] + "\n... [content truncated]"

                context_parts.append(f"File content:\n{content}")

    context_parts.append(f"Assistant: {exchange.raw_answer}")

    return context_parts


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
                context_parts = _append_context_parts(
                    context_parts, exchange, file_content
                )

            context = "\n\n".join(context_parts) + "\n\n"

    full_prompt = SYSTEM_PROMPT

    if context:
        full_prompt += f"\n\nPrevious conversation:\n{context}"

    current_prompt = prompt

    if file_content:
        content_to_include = file_content

        if len(file_content) > 30000:  # pragma: no cover
            content_to_include = (
                file_content[:30000] + "\n... [content truncated]"
            )  # noqa: E501

        current_prompt = f"""User query: {prompt}

[Attached file content]
{content_to_include}

Please consider the attached file content when answering the query above."""

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

    try:
        r = requests.post(url, json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        return (data.get("response") or "").strip()

    except requests.exceptions.ConnectionError:  # pragma: no cover
        return "LLM unavailable. Is Ollama running on 127.0.0.1:11434?"
    except requests.exceptions.Timeout:  # pragma: no cover
        return "LLM request timed out."
    except Exception as exc:  # pragma: no cover
        return f"LLM error: {exc}"
