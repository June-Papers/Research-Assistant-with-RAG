from pathlib import Path
from typing import Dict, Optional


class ReportMetadata:
    """Build metadata for stored report segments."""

    def __init__(self, company: str, year: int, quarter: str, report_type: str, rcept_no: str, filepath: str) -> None:
        self.company = company
        self.year = year
        self.quarter = quarter
        self.report_type = report_type
        self.rcept_no = rcept_no
        self.filepath = filepath

    def to_dict(self) -> Dict[str, object]:
        """Convert metadata to a dictionary."""
        return {
            "company": self.company,
            "year": self.year,
            "quarter": self.quarter,
            "report_type": self.report_type,
            "rcept_no": self.rcept_no,
            "filepath": self.filepath,
        }
