import re
from typing import Dict, Optional, Tuple


class QueryParser:
    """Parse a natural language question for company, years, and requested data."""

    def __init__(self) -> None:
        pass

    def parse(self, query: str) -> Dict[str, Optional[object]]:
        """Extract company name, start year, end year, and requested data from a query."""
        company_match = re.search(r"([가-힣A-Za-z0-9]+)", query)
        company = company_match.group(1) if company_match else None
        years = re.findall(r"(20\d{2})", query)
        start_year = int(years[0]) if len(years) >= 1 else None
        end_year = int(years[-1]) if len(years) >= 2 else start_year
        requested_data = query.split("로")[-1].strip() if "로" in query else query
        return {
            "company": company,
            "start_year": start_year,
            "end_year": end_year,
            "requested_data": requested_data,
        }
