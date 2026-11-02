import logging

import aisuite as ai
import gradio as gr

from resume_agent.agent.agent import ResumeAgent
from resume_agent.config import Settings
from resume_agent.repositories.resume_repository import ResumeRepository
from resume_agent.tools.github_tools import build_github_tools
from resume_agent.tools.resume_tools import build_resume_tool


def create_llm_client(settings: Settings) -> ai.Client:
    """Create a client for an OpenAI-compatible API."""

    config = {}

    if settings.provider_api_key:
        config["api_key"] = settings.provider_api_key

    if settings.provider_base_url:
        config["base_url"] = settings.provider_base_url

    if not config:
        return ai.Client()

    return ai.Client(provider_configs={"openai": config})


def build_app(settings: Settings | None = None) -> gr.ChatInterface:
    """Initialize dependencies and build the Gradio application."""

    settings = settings or Settings.from_env()

    # Build GitHub tools
    github_tools = (
        build_github_tools(settings.github_username)
        if settings.github_username
        else []
    )

    # Initialize resume repository
    repository = ResumeRepository(settings.resume_path)
    repository.ensure_exists()

    # Build tools
    resume_tool = build_resume_tool(repository)

    # Initialize LLM client
    client = create_llm_client(settings)

    # Initialize agent
    agent = ResumeAgent(
        client=client,
        model=settings.provider_code,
        tools=[resume_tool, *github_tools],
        max_tool_turns=settings.max_tool_turns,
        max_history_messages=settings.max_history_messages,
        temperature=settings.temperature,
    )

    # Build Gradio interface
    return gr.ChatInterface(
        fn=agent.chat,
        title="Resume & Career Portfolio Assistant",
        description=(
            "Ask questions about the person's professional "
            "background, skills, experience, education, and projects."
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
    app.launch(footer_links=[])
