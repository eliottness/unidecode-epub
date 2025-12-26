"""Tests for the CLI interface."""

import os
import tempfile
import pytest
from ebooklib import epub
from unidecode_epub.cli import main
import sys


def create_test_epub(path: str, title: str = "Test Book", content: str = "Test content"):
    """Helper function to create a test EPUB file."""
    book = epub.EpubBook()
    book.set_title(title)
    book.add_author("Test Author")
    book.set_language('en')
    
    chapter = epub.EpubHtml(
        title='Chapter 1',
        file_name='chap_01.xhtml',
        lang='en'
    )
    chapter.content = f'<h1>Chapter 1</h1><p>{content}</p>'
    book.add_item(chapter)
    
    book.toc = (epub.Link('chap_01.xhtml', 'Chapter 1', 'chap1'),)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav', chapter]
    
    epub.write_epub(path, book)


class TestCLI:
    """Test cases for CLI interface."""
    
    def test_cli_with_valid_input(self, monkeypatch, capsys):
        """Test CLI with a valid EPUB file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, 'test_input.epub')
            create_test_epub(input_path, content="Hello World")
            
            # Mock sys.argv
            monkeypatch.setattr(sys, 'argv', ['unidecode-epub', input_path])
            
            exit_code = main()
            
            assert exit_code == 0
            captured = capsys.readouterr()
            assert 'Successfully processed EPUB file' in captured.out
            assert input_path in captured.out
    
    def test_cli_with_custom_output(self, monkeypatch, capsys):
        """Test CLI with custom output path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, 'test_input.epub')
            output_path = os.path.join(tmpdir, 'custom_output.epub')
            create_test_epub(input_path)
            
            monkeypatch.setattr(sys, 'argv', [
                'unidecode-epub',
                input_path,
                '-o', output_path
            ])
            
            exit_code = main()
            
            assert exit_code == 0
            assert os.path.exists(output_path)
            captured = capsys.readouterr()
            assert output_path in captured.out
    
    def test_cli_with_nonexistent_file(self, monkeypatch, capsys):
        """Test CLI error handling for non-existent file."""
        monkeypatch.setattr(sys, 'argv', [
            'unidecode-epub',
            '/nonexistent/file.epub'
        ])
        
        exit_code = main()
        
        assert exit_code == 1
        captured = capsys.readouterr()
        assert 'Error' in captured.err
    
    def test_cli_with_invalid_epub(self, monkeypatch, capsys):
        """Test CLI error handling for invalid EPUB."""
        with tempfile.TemporaryDirectory() as tmpdir:
            invalid_path = os.path.join(tmpdir, 'invalid.epub')
            with open(invalid_path, 'w') as f:
                f.write("Not an EPUB")
            
            monkeypatch.setattr(sys, 'argv', [
                'unidecode-epub',
                invalid_path
            ])
            
            exit_code = main()
            
            assert exit_code == 1
            captured = capsys.readouterr()
            assert 'Error' in captured.err
    
    def test_cli_help(self, monkeypatch):
        """Test CLI help message."""
        monkeypatch.setattr(sys, 'argv', ['unidecode-epub', '--help'])
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
    
    def test_cli_version(self, monkeypatch):
        """Test CLI version output."""
        monkeypatch.setattr(sys, 'argv', ['unidecode-epub', '--version'])
        
        with pytest.raises(SystemExit) as exc_info:
            main()
        
        assert exc_info.value.code == 0
