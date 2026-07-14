from typing import List


class PromptBuilder:
    """Build a prompt for the LLM using retrieved chunks."""

    def __init__(self) -> None:
        pass

    def build(self, query: str, retrieved_chunks: List[str]) -> str:
        """Create a structured prompt for the LLM."""
        context = "\n\n".join(retrieved_chunks)
        return f"""You are an expert financial analyst.
You will receive report excerpts and a user question.
Extract the requested information and return ONLY a JSON object.

User question:
{query}

Report excerpts:
{context}

Return JSON with keys: company, year, quarter, report_type, metric, value, unit, notes.
If a value is not found, use null.
"""
