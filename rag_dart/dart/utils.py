import logging
import os
import time
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


def configure_logging(log_dir: str = "logs") -> None:
    """Set up basic logging configuration for the project."""
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(log_dir, "rag_dart.log"), encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def request_with_retry(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
    max_retries: int = 3,
) -> requests.Response:
    """Call a URL with retry and timeout handling."""
    last_error: Optional[Exception] = None
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as exc:
            last_error = exc
            logger.warning("Request failed for %s (attempt %s/%s): %s", url, attempt, max_retries, exc)
            time.sleep(2)
    raise RuntimeError(f"Request failed after {max_retries} attempts: {last_error}")
