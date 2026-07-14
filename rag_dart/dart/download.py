import os
import zipfile
from pathlib import Path
from typing import Dict, List, Optional

import requests

from config import DART_API_KEY
from dart.utils import logger, request_with_retry


class ReportDownloader:
    """Download DART report documents and unzip them."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def download_report(self, rcept_no: str, output_dir: str) -> Optional[str]:
        """Download the zip file for a report and extract contents."""
        url = "https://opendart.fss.or.kr/api/document.xml"
        params = {"crtfc_key": self.api_key, "rcept_no": rcept_no}
        response = request_with_retry(url, params=params)
        xml_text = response.text
        zip_path = os.path.join(output_dir, f"{rcept_no}.zip")
        with open(zip_path, "wb") as handle:
            handle.write(response.content)

        extract_dir = os.path.join(output_dir, rcept_no)
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as archive:
            archive.extractall(extract_dir)
        return extract_dir
