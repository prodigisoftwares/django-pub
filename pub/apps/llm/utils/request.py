import requests
from django.conf import settings

TIMEOUT = settings.OLLAMA_TIMEOUT


def post_prompt(prompt: str, url: str, payload: dict) -> str:
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
