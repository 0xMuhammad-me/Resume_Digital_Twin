import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _get_int(name: str, default: int) -> int:
    """Read an integer environment variable."""
    raw_value = os.getenv(name, str(default)).strip()

    try:
        return int(raw_value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a valid integer. Got: {raw_value!r}") from exc


def _get_float(name: str, default: float) -> float:
    """Read a float environment variable."""
    raw_value = os.getenv(name, str(default)).strip()

    try:
        return float(raw_value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a valid number. Got: {raw_value!r}") from exc


@dataclass(frozen=True, slots=True)
class Settings:
    """Application configuration."""

    provider_code: str
    provider_base_url: str | None
    provider_api_key: str | None

    github_username: str | None
    resume_path: Path

    max_tool_turns: int = 3
    max_history_messages: int = 20
    temperature: float = 0.2

    @classmethod
    def from_env(cls) -> "Settings":
        """Load and validate application settings."""

        load_dotenv(dotenv_path=PROJECT_ROOT / ".env", override=False)

        # Provider configuration
        provider_code = os.getenv("PROVIDER_CODE", "").strip()

        if not provider_code:
            raise RuntimeError("PROVIDER_CODE must be defined in the .env file.")

        provider, separator, model_name = provider_code.partition(":")

        if not separator or not provider.strip() or not model_name.strip():
            raise ValueError("PROVIDER_CODE must use 'openai:model-name' format.")

        if provider != "openai":
            raise ValueError("Only the 'openai' provider is currently supported.")

        provider_base_url = os.getenv("PROVIDER_BASE_URL", "").strip() or None

        if provider_base_url:
            provider_base_url = provider_base_url.rstrip("/")

        provider_api_key = os.getenv("PROVIDER_API_KEY", "").strip() or None

        # GitHub configuration
        github_username = os.getenv("GITHUB_USERNAME", "").strip() or None

        # Resume configuration
        resume_path_raw = os.getenv("RESUME_PATH", "data/Resume.pdf").strip()

        if not resume_path_raw:
            resume_path_raw = "data/Resume.pdf"

        resume_path = Path(resume_path_raw).expanduser()

        if not resume_path.is_absolute():
            resume_path = PROJECT_ROOT / resume_path

        resume_path = resume_path.resolve()

        # Agent configuration
        max_tool_turns = _get_int("MAX_TOOL_TURNS", 3)
        max_history_messages = _get_int("MAX_HISTORY_MESSAGES", 20)
        temperature = _get_float("TEMPERATURE", 0.2)

        if max_tool_turns < 1:
            raise ValueError("MAX_TOOL_TURNS must be at least 1.")

        if max_history_messages < 0:
            raise ValueError("MAX_HISTORY_MESSAGES cannot be negative.")

        if not 0 <= temperature <= 2:
            raise ValueError("TEMPERATURE must be between 0 and 2.")

        return cls(
            provider_code=provider_code,
            provider_base_url=provider_base_url,
            provider_api_key=provider_api_key,
            github_username=github_username,
            resume_path=resume_path,
            max_tool_turns=max_tool_turns,
            max_history_messages=max_history_messages,
            temperature=temperature,
        )
