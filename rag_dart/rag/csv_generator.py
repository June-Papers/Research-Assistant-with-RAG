import json
import os
from typing import Any, Dict, List

import pandas as pd


class CSVGenerator:
    """Generate a CSV from aggregated LLM results."""

    def __init__(self, output_dir: str = "reports") -> None:
        self.output_dir = output_dir

    def save_csv(self, rows: List[Dict[str, Any]], file_name: str = "result.csv") -> str:
        """Save aggregated rows as UTF-8-SIG CSV."""
        os.makedirs(self.output_dir, exist_ok=True)
        path = os.path.join(self.output_dir, file_name)
        df = pd.DataFrame(rows)
        df.to_csv(path, index=False, encoding="utf-8-sig")
        return path
