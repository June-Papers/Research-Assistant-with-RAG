import os
from dotenv import load_dotenv

load_dotenv()


def require_env() -> None:
    """Ensure required environment variables are present."""
    provider = (os.getenv("LLM_PROVIDER") or "openai").lower()
    required = ["DART_API_KEY"]
    if provider == "openai":
        required.append("OPENAI_API_KEY")
    elif provider == "gemini":
        required.append("GEMINI_API_KEY")
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {os.getenv('LLM_PROVIDER')}")

    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")


require_env()

DART_API_KEY = os.getenv("DART_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
LLM_PROVIDER = (os.getenv("LLM_PROVIDER") or "openai").lower()
