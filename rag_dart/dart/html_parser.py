import json
import os
import re
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Tuple


class HTMLTextParser:
    """Parse HTML/XML content into plain text while preserving table content."""

    def __init__(self) -> None:
        self._remove_tags = {"script", "style", "noscript"}

    def parse_file(self, file_path: str) -> Dict[str, object]:
        """Parse an HTML/XML file into text and table data."""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as handle:
            content = handle.read()
        soup = BeautifulSoup(content, "lxml")
        for tag in soup(self._remove_tags):
            tag.decompose()

        text_parts: List[str] = []
        table_parts: List[Dict[str, object]] = []

        for element in soup.find_all(["p", "li", "div", "span", "h1", "h2", "h3", "h4", "section"]):
            text = self._clean_text(element.get_text("\n", strip=True))
            if text:
                text_parts.append(text)

        for table in soup.find_all("table"):
            table_data = self._table_to_markdown(table)
            if table_data:
                table_parts.append({"markdown": table_data, "raw_html": str(table)})

        return {
            "text": "\n\n".join(text_parts),
            "tables": table_parts,
        }

    def _clean_text(self, text: str) -> str:
        """Clean extracted text and collapse whitespace."""
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _table_to_markdown(self, table) -> str:
        """Convert a table element to a markdown table."""
        rows = []
        for row in table.find_all("tr"):
            cells = [self._clean_text(cell.get_text(" ", strip=True)) for cell in row.find_all(["th", "td"])]
            if cells:
                rows.append(cells)
        if not rows:
            return ""
        header = rows[0]
        separator = ["-" * max(len(cell), 3) for cell in header]
        markdown_rows = ["| " + " | ".join(header) + " |", "| " + " | ".join(separator) + " |"]
        for row in rows[1:]:
            markdown_rows.append("| " + " | ".join(row) + " |")
        return "\n".join(markdown_rows)
