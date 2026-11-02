from pathlib import Path

from pypdf import PdfReader


class ResumeRepository:
    """Load resume text from a PDF, caching it after the first read."""

    def __init__(self, pdf_path: str | Path) -> None:
        self._pdf_path = Path(pdf_path).expanduser().resolve()
        self._cached_text: str | None = None

    @property
    def pdf_path(self) -> Path:
        """Return the resolved path to the source PDF."""
        return self._pdf_path

    def ensure_exists(self) -> None:
        """Fail early if the configured PDF path does not exist."""
        if not self._pdf_path.is_file():
            raise FileNotFoundError(f"Resume PDF was not found: {self._pdf_path}")

    def get_resume_text(self) -> str:
        """Return extracted resume text, reading the PDF only once per process."""
        if self._cached_text is not None:
            return self._cached_text

        self.ensure_exists()
        reader = PdfReader(str(self._pdf_path))
        page_texts = [
            text.strip()
            for page in reader.pages
            if (text := page.extract_text()) and text.strip()
        ]
        resume_text = "\n\n".join(page_texts).strip()

        if not resume_text:
            raise ValueError(
                "No extractable text was found in the resume PDF. "
                "If it is a scanned PDF, OCR is required."
            )

        self._cached_text = resume_text
        return resume_text
