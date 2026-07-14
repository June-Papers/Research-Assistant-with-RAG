import json
from typing import List, Dict, Optional

from config import DART_API_KEY
from dart.utils import logger, request_with_retry


class ReportListClient:
    """Client for retrieving DART report lists."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def get_reports(
        self,
        corp_code: str,
        start_year: int,
        end_year: int,
        bgn_de: str = "20200101",
        end_de: str = "20301231",
    ) -> List[Dict[str, str]]:
        """Retrieve annual report list for the company."""
        reports: List[Dict[str, str]] = []
        url = "https://opendart.fss.or.kr/api/list.json"
        params = {
            "crtfc_key": self.api_key,
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
            "page_no": 1,
            "page_count": 100,
        }
        response = request_with_retry(url, params=params)
        payload = response.json()
        if payload.get("status") != "000":
            raise RuntimeError(f"DART API error: {payload}")

        for item in payload.get("list", []):
            report_year = item.get("rcept_dt", "")[:4]
            if start_year <= int(report_year) <= end_year:
                report_type = item.get("report_nm", "")
                if any(keyword in report_type for keyword in ["사업보고서", "반기보고서", "분기보고서"]):
                    reports.append(
                        {
                            "rcept_no": item.get("rcept_no", ""),
                            "report_type": report_type,
                            "rcept_dt": item.get("rcept_dt", ""),
                            "corp_name": item.get("corp_name", ""),
                        }
                    )
        return reports
