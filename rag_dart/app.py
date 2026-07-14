import json
import os
from typing import Any, Dict, List

from config import OPENAI_API_KEY
from dart.utils import configure_logging, logger
from rag.csv_generator import CSVGenerator
from rag.embedding import EmbeddingClient
from rag.llm.factory import get_llm
from rag.prompt import PromptBuilder
from rag.query_parser import QueryParser
from rag.retrieval import Retriever
from rag.vectordb import VectorDB

configure_logging("logs")


def run_query(query: str) -> str:
    """Run a user query end-to-end and save a CSV file."""
    parser = QueryParser()
    parsed = parser.parse(query)
    company = parsed.get("company")
    start_year = parsed.get("start_year")
    end_year = parsed.get("end_year")
    if not company or not start_year or not end_year:
        raise ValueError("Could not parse company name and years from the query")

    vector_db = VectorDB("vector_db")
    embedding_client = EmbeddingClient(OPENAI_API_KEY)
    retriever = Retriever(vector_db, embedding_client)
    prompt_builder = PromptBuilder()
    csv_generator = CSVGenerator("reports")

    rows: List[Dict[str, Any]] = []
    for year in range(start_year, end_year + 1):
        for quarter in ["Q1", "Q2", "Q3", "Q4"]:
            where_filter = {
                "$and": [
                    {"company": company},
                    {"year": year},
                    {"quarter": quarter},
                ]
            }
            result = retriever.retrieve(query, metadata_filter=where_filter, top_k=3)
            if not result.get("documents"):
                continue
            retrieved_chunks = []
            for chunk in result["documents"][0]:
                if chunk:
                    retrieved_chunks.append(chunk)
            if not retrieved_chunks:
                continue

            prompt = prompt_builder.build(query, retrieved_chunks)
            provider = get_llm()
            content = provider.generate(prompt)
            try:
                parsed_json = json.loads(content)
            except json.JSONDecodeError:
                parsed_json = {"company": company, "year": year, "quarter": quarter, "metric": None, "value": None, "unit": None, "notes": content}
            row = {
                "company": company,
                "year": year,
                "quarter": quarter,
                "report_type": parsed_json.get("report_type"),
                "metric": parsed_json.get("metric"),
                "value": parsed_json.get("value"),
                "unit": parsed_json.get("unit"),
                "notes": parsed_json.get("notes"),
            }
            rows.append(row)

    output_path = csv_generator.save_csv(rows, f"{company}_results.csv")
    return output_path


if __name__ == "__main__":
    question = input("질문 입력 : ").strip()
    output_path = run_query(question)
    print(f"CSV 생성 완료: {output_path}")
