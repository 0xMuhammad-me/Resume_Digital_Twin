---
title: Resume Digital Twin
emoji: 📄
colorFrom: blue
colorTo: indigo
sdk: gradio
app_file: app.py
python_version: 3.12
---

# Resume Digital Twin

An AI-powered professional portfolio assistant built with **Gradio** and **AISuite**. It acts as an AI digital twin of a professional and answers questions about their career, education, skills, experience, and documented projects using their resume and configured public GitHub repositories as reference sources.

The assistant can use a natural first-person voice, but it must be transparent that it is an AI and must not claim to be the actual person.

## Features

- **Resume-grounded answers:** retrieves professional information from `data/Resume.pdf` through the `get_resume` tool.
- **Public GitHub context:** can discover public repositories and read repository READMEs when GitHub tools are configured.
- **Professional scope:** is designed to focus on the represented person's career, qualifications, contact details intended for public professional use, and documented projects.
- **Multilingual responses:** responds in the language of the latest user message, depending on the configured model's capabilities.
- **Prompt-injection precautions:** treats the resume, GitHub content, conversation history, and tool outputs as untrusted data rather than instructions.
- **Gradio chat interface:** provides a browser-based conversational UI.

> **Important:** Model-based scope checks and prompt-injection instructions reduce risk but are not security guarantees. Review the application before exposing it to public users.

## How it works

1. The user sends a message through the Gradio interface.
2. The application sends the conversation to the configured language model through AISuite.
3. When needed, the assistant calls `get_resume` to retrieve resume text.
4. If GitHub integration is enabled, it can list public repositories or retrieve a repository README for project-specific questions.
5. The assistant produces an answer grounded in the available sources and should state when a fact cannot be verified.

The resume is the primary source for employment, education, and professional claims. GitHub is a supplementary source for public project documentation and repository details.

## Limitations

- Answers depend on the information available in the resume, public repository metadata, and project documentation.
- The assistant should not infer or invent missing experience, qualifications, achievements, or contact information.
- Model responses and automated scope checks may be imperfect; important claims should be verified against the source documents.
- Availability, latency, and operating cost depend on the selected model provider and Hugging Face Space configuration.

## License

Add a license before redistributing this project. Make sure you have permission to publish the resume and any other personal or third-party content included with the application.
