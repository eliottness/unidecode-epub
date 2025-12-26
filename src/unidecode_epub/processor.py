"""EPUB processor module for converting Unicode text to ASCII."""

import os
from typing import Optional
from ebooklib import epub
from unidecode import unidecode


def process_epub(input_path: str, output_path: Optional[str] = None) -> str:
    """
    Process an EPUB file by converting all Unicode text to ASCII using unidecode.
    
    Args:
        input_path: Path to the input EPUB file
        output_path: Path to the output EPUB file. If None, generates a name based on input.
    
    Returns:
        Path to the output EPUB file
    
    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If input file is not a valid EPUB
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Generate output path if not provided
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_ascii{ext}"
    
    # Read the EPUB file
    try:
        book = epub.read_epub(input_path)
    except Exception as e:
        raise ValueError(f"Failed to read EPUB file: {e}")
    
    # Process each item in the book
    for item in book.get_items():
        # Process HTML/XHTML content (main document content)
        if isinstance(item, epub.EpubHtml):
            content = item.get_content().decode('utf-8')
            # Convert Unicode to ASCII
            ascii_content = unidecode(content)
            item.set_content(ascii_content.encode('utf-8'))
        
        # Process other items with content (navigation, etc.)
        elif hasattr(item, 'get_content') and hasattr(item, 'set_content'):
            try:
                content = item.get_content().decode('utf-8')
                ascii_content = unidecode(content)
                item.set_content(ascii_content.encode('utf-8'))
            except (UnicodeDecodeError, AttributeError):
                # Skip binary content or items that can't be decoded
                pass
    
    # Convert metadata
    title = book.get_metadata('DC', 'title')
    if title:
        book.set_title(unidecode(title[0][0]))
    
    # Process TOC to ensure UIDs are set properly
    def fix_toc_uids(toc, counter=[0]):
        """Recursively fix UIDs in TOC structure."""
        result = []
        for item in toc:
            if isinstance(item, tuple):
                # Nested section
                section, children = item[0], item[1:]
                fixed_children = fix_toc_uids(children, counter)
                result.append((section, *fixed_children))
            elif isinstance(item, epub.Link):
                # Ensure Link has a UID
                if not hasattr(item, 'uid') or item.uid is None:
                    item.uid = f'navpoint_{counter[0]}'
                    counter[0] += 1
                result.append(item)
            elif isinstance(item, epub.Section):
                # Ensure Section has a UID
                if not hasattr(item, 'uid') or item.uid is None:
                    item.uid = f'navpoint_{counter[0]}'
                    counter[0] += 1
                result.append(item)
            else:
                result.append(item)
        return result
    
    if hasattr(book, 'toc') and book.toc:
        book.toc = fix_toc_uids(book.toc)
    
    # Write the output EPUB file
    try:
        epub.write_epub(output_path, book)
    except Exception as e:
        raise ValueError(f"Failed to write EPUB file: {e}")
    
    return output_path
