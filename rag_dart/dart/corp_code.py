import os
import zipfile
from typing import Dict, List, Optional

import requests

from config import DART_API_KEY
from dart.utils import logger, request_with_retry


class CorpCodeClient:
    """Client for retrieving DART corp codes."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def download_corp_code_xml(self, output_path: str) -> str:
        """Download the corp code XML file from DART."""
        url = "https://opendart.fss.or.kr/api/corpCode.xml"
        params = {"crtfc_key": self.api_key}
        response = request_with_retry(url, params=params)
        with open(output_path, "wb") as handle:
            handle.write(response.content)
        return output_path

    def find_corp_code(self, company_name: str, corp_code_path: str) -> Optional[str]:
        """Find a corporation code by company name from the XML file."""
        if not os.path.exists(corp_code_path):
            raise FileNotFoundError(f"Corp code file not found: {corp_code_path}")

        import xml.etree.ElementTree as ET

        tree = ET.parse(corp_code_path)
        root = tree.getroot()
        for item in root.findall("./list"):
            corp_name = item.findtext("corp_name")
            corp_code = item.findtext("corp_code")
            if corp_name and corp_name.strip() == company_name.strip():
                return corp_code
        return None
