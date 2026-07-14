import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from config import DART_API_KEY, OPENAI_API_KEY, OPENAI_MODEL
from dart.corp_code import CorpCodeClient
from dart.download import ReportDownloader
from dart.html_parser import HTMLTextParser
from dart.metadata import ReportMetadata
from dart.report_list import ReportListClient
from dart.utils import configure_logging, logger
from rag.chunk import DocumentChunker
from rag.embedding import EmbeddingClient
from rag.vectordb import VectorDB

configure_logging("logs")


def build_vector_db(company_name: str, start_year: int, end_year: int) -> str:
    """Build a ChromaDB index from DART reports for the requested company and years."""
    reports_dir = os.path.join("reports", company_name)
    os.makedirs(reports_dir, exist_ok=True)

    corp_code_path = os.path.join("reports", f"{company_name}_corp_code.xml")
    corp_client = CorpCodeClient(DART_API_KEY)
    corp_client.download_corp_code_xml(corp_code_path)
    corp_code = corp_client.find_corp_code(company_name, corp_code_path)
    if not corp_code:
        raise ValueError(f"Corp code not found for {company_name}")

    list_client = ReportListClient(DART_API_KEY)
    reports = list_client.get_reports(corp_code, start_year, end_year)

    downloader = ReportDownloader(DART_API_KEY)
    parser = HTMLTextParser()
    chunker = DocumentChunker()
    embedding_client = EmbeddingClient(OPENAI_API_KEY)
    vector_db = VectorDB("vector_db")

    documents: List[str] = []
    metadatas: List[Dict[str, Any]] = []
    ids: List[str] = []

    for report in reports:
        report_type = report["report_type"]
        quarter = "Q4"
        if "반기보고서" in report_type:
            quarter = "Q2"
        elif "분기보고서" in report_type:
            quarter = "Q1"

        report_year = int(report["rcept_dt"][:4])
        report_dir = os.path.join(reports_dir, str(report_year), quarter)
        os.makedirs(report_dir, exist_ok=True)
        extract_dir = downloader.download_report(report["rcept_no"], report_dir)
        if not extract_dir:
            continue

        for root, _, files in os.walk(extract_dir):
            for file_name in files:
                if not file_name.lower().endswith((".html", ".htm", ".xml", ".xhtml")):
                    continue
                file_path = os.path.join(root, file_name)
                try:
                    parsed = parser.parse_file(file_path)
                except Exception as exc:
                    logger.warning("Failed to parse %s: %s", file_path, exc)
                    continue

                combined_text = parsed["text"]
                if isinstance(parsed.get("tables"), list):
                    for table in parsed["tables"]:
                        if isinstance(table, dict):
                            combined_text += f"\n\nTABLE:\n{table.get('markdown', '')}"
                chunks = chunker.split_text(combined_text)
                for chunk_index, chunk in enumerate(chunks):
                    chunk_path = os.path.join(report_dir, f"{file_name}_{chunk_index}.txt")
                    with open(chunk_path, "w", encoding="utf-8") as handle:
                        handle.write(chunk)
                    metadata = ReportMetadata(
                        company=company_name,
                        year=report_year,
                        quarter=quarter,
                        report_type=report_type,
                        rcept_no=report["rcept_no"],
                        filepath=chunk_path,
                    ).to_dict()
                    documents.append(chunk)
                    metadatas.append(metadata)
                    ids.append(f"{company_name}_{report_year}_{quarter}_{report['rcept_no']}_{chunk_index}")

    if not documents:
        raise RuntimeError("No documents were collected for the requested company")

    embeddings = embedding_client.embed_texts(documents)
    for idx, embedding in enumerate(embeddings):
        vector_db.add_documents([documents[idx]], [metadatas[idx]], [ids[idx]])
    return os.path.abspath("vector_db")


if __name__ == "__main__":
    company = input("기업명 : ").strip()
    start_year = int(input("시작년도 : ").strip())
    end_year = int(input("종료년도 : ").strip())
    build_vector_db(company, start_year, end_year)
    print("VectorDB 구축 완료")
