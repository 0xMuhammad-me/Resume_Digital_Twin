import logging
import os
from pathlib import Path

import aisuite as ai
import gradio as gr
from dotenv import load_dotenv

from resume_agent import ResumeAgent
from resume_repository import ResumeRepository
from resume_tools import build_resume_tool
from github_tools import build_github_tools

BASE_DIR = Path(__file__).resolve().parent


def create_llm_client(model_code: str, base_url: str | None, api_key: str | None) -> ai.Client:
    """Create a client for an OpenAI-compatible API."""

    provider, separator, _model_name = model_code.partition(":")

    if not separator or not provider.strip() or not _model_name.strip():
        raise ValueError("PROVIDER_CODE must use 'openai:model-name' format.")

    if provider != "openai":
        raise ValueError("For a custom OpenAI-compatible endpoint, set PROVIDER_CODE=openai:model-name.")

    config = {}

    if api_key:
        config["api_key"] = api_key

    if base_url:
        config["base_url"] = base_url.rstrip("/")

    if not config:
        return ai.Client()

    return ai.Client(provider_configs={"openai": config})


def build_app() -> gr.ChatInterface:
    load_dotenv()

    github_username = os.getenv("GITHUB_USERNAME", "").strip()

    github_tools = (build_github_tools(github_username) if github_username else [])
    model_code = os.getenv("PROVIDER_CODE", "").strip()
    if not model_code:
        raise RuntimeError("Set PROVIDER_CODE in your .env file.")

    base_url = os.getenv("PROVIDER_BASE_URL")
    api_key = os.getenv("PROVIDER_API_KEY")
    resume_path = Path(os.getenv("RESUME_PATH", "Resume.pdf")).expanduser()
    if not resume_path.is_absolute():
        resume_path = BASE_DIR / resume_path

    repository = ResumeRepository(resume_path)
    repository.ensure_exists()

    resume_tool = build_resume_tool(repository)
    client = create_llm_client(model_code, base_url, api_key)
    agent = ResumeAgent(
        client=client,
        model=model_code,
        tools=[resume_tool, *github_tools],
        max_tool_turns=3,
        max_history_messages=20,
        temperature=0.2,
    )

    return gr.ChatInterface(
        fn=agent.chat,
        title="Resume & Career Portfolio Assistant",
        description=(
            "Ask questions about the person's professional background, skills, "
            "experience, education, and projects."
        ),
        examples=[
            "Tell me about your professional background.",
            "What are your main technical skills?",
            "Can you summarize your projects?",
        ],
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = build_app()
    app.launch(inbrowser=True, footer_links=[])
