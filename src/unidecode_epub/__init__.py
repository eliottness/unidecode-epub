"""unidecode-epub: CLI tool to convert Unicode text in EPUB files to ASCII."""

from .processor import process_epub
from .cli import main

__version__ = "0.1.0"
__all__ = ["process_epub", "main"]
