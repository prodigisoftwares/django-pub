def add_file_context(prompt: str, file_content: str) -> str:
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
