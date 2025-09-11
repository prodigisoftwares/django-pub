"""
This module provides utility functions for constructing and
managing conversational context for LLM (Large Language Model)
interactions. It includes helpers to format user queries,
attach file contents, and build context histories from previous
exchanges, enabling more context-aware and relevant responses
from the assistant.
"""


def add_file_context(prompt: str, file_content: str) -> str:
    """
    Adds the content of a file to a user prompt for context-aware processing.

    If the file content exceeds 30,000 characters, it truncates the content
    and appends a notice.

    Args:
        prompt (str): The user's query or prompt.
        file_content (str): The content of the file to include.

    Returns:
        str: The prompt with the attached file content for further processing.
    """
    content_to_include = file_content

    if len(file_content) > 30000:  # pragma: no cover
        content_to_include = (
            file_content[:30000] + "\n... [content truncated]"
        )  # noqa: E501

    current_prompt = f"""User query: {prompt}

[Attached file content]
{content_to_include}

Please consider the attached file content when answering the query above."""
    return current_prompt


def append_context_parts(
    context_parts: list[str], exchange, file_content: str | None
) -> list[str]:
    """
    Appends user and assistant exchanges, along with any attached file
    content, to the context parts list.

    If file_content is not provided, it checks for attachments in the
    exchange and includes their content (truncated if necessary).

    Args:
        context_parts (list[str]): The list to append context strings to.
        exchange: The exchange object containing user query, attachments,
        and assistant answer.
        file_content (str | None): Optional file content to include.

    Returns:
        list[str]: The updated list of context parts.
    """
    context_parts.append(f"User: {exchange.query}")

    if not file_content:
        attachments = exchange.attachments.all()

        if attachments:
            for attachment in attachments:
                context_parts.append(
                    f"[Attached file: {attachment.filename}]",
                )

                content = attachment.content

                if len(content) > 3000:  # pragma: no cover
                    content = content[:3000] + "\n... [content truncated]"

                context_parts.append(f"File content:\n{content}")

    context_parts.append(f"Assistant: {exchange.raw_answer}")

    return context_parts


def get_context(
    conversation, file_content: str = None
) -> str:  # pragma: no cover  # noqa: C901
    """
    Builds a string representing the context of a conversation, including
    previous exchanges and optional file content.

    Retrieves up to 10 previous exchanges, appending user queries,
    assistant answers, and any attached file content.

    Args:
        conversation: The conversation object containing exchanges.
        file_content (str, optional): Optional file content to include in
        the context.

    Returns:
        str: The constructed context string for the conversation.
    """
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

    return context
