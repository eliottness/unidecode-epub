# unidecode-epub

A Python CLI tool to convert Unicode text in EPUB files to ASCII, making them compatible with old MOBI-only Amazon Kindle devices.

## Overview

`unidecode-epub` processes EPUB files by converting all Unicode characters to their closest ASCII equivalents using the [unidecode](https://github.com/avian2/unidecode) library. This is particularly useful for preparing ebooks for older Kindle devices that don't handle Unicode characters well, especially in filenames, metadata, or content.

## Features

- ✨ Converts all Unicode text in EPUB content to ASCII
- 📚 Processes HTML/XHTML content within EPUB files
- 🏷️ Handles metadata conversion
- 🔧 Simple command-line interface
- ✅ Comprehensive test coverage
- 🚀 Fast and efficient processing

## Installation

You can install `unidecode-epub` directly from PyPI using pip:

```bash
pip install unidecode-epub
```

### Installation from Source

Alternatively, you can install from source:

```bash
git clone https://github.com/eliottness/unidecode-epub.git
cd unidecode-epub
pip install .
```

### Development Installation

For development with uv:

```bash
git clone https://github.com/eliottness/unidecode-epub.git
cd unidecode-epub
uv sync
```

## Usage

### Command Line

After installation, you can use the `unidecode-epub` command:

```bash
# Basic usage - converts input.epub to input_ascii.epub
unidecode-epub input.epub

# Specify custom output path
unidecode-epub input.epub -o output.epub

# Show help
unidecode-epub --help

# Show version
unidecode-epub --version
```

### Python API

You can also use `unidecode-epub` as a Python library:

```python
from unidecode_epub import process_epub

# Process an EPUB file
output_path = process_epub('input.epub')
print(f"Processed EPUB saved to: {output_path}")

# Specify custom output path
output_path = process_epub('input.epub', 'custom_output.epub')
```

## Examples

### Example 1: Converting a Book with Unicode Characters

```bash
$ unidecode-epub "Café_Society_by_José_García.epub"
Successfully processed EPUB file.
Input:  /home/user/books/Café_Society_by_José_García.epub
Output: /home/user/books/Café_Society_by_José_García_ascii.epub
```

The output file will have all Unicode characters converted:
- `Café` → `Cafe`
- `José García` → `Jose Garcia`
- `北京` → `Bei Jing`
- `naïve` → `naive`

### Example 2: Processing Multiple Files

```bash
# Process multiple EPUB files in a directory
for file in *.epub; do
    unidecode-epub "$file"
done
```

## How It Works

1. **Read EPUB**: The tool reads the input EPUB file using the `ebooklib` library
2. **Process Content**: All HTML/XHTML content is decoded and processed through `unidecode`
3. **Convert Text**: Unicode characters are converted to their closest ASCII equivalents
4. **Fix Structure**: TOC (Table of Contents) structure is fixed to ensure valid EPUB output
5. **Write Output**: The processed content is written to a new EPUB file

## Requirements

- Python 3.8 or higher
- Dependencies:
  - `unidecode>=1.4.0` - For Unicode to ASCII conversion
  - `ebooklib>=0.20` - For EPUB file handling

## Development

### Running Tests

```bash
# With uv
uv run pytest tests/

# With standard Python
pip install pytest
pytest tests/
```

### Building the Package

```bash
# With uv
uv build

# With standard Python build tools
pip install build
python -m build
```

## License

This project is licensed under the GNU General Public License v2.0 or later (GPL-2.0-or-later). See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [unidecode](https://github.com/avian2/unidecode) - For the Unicode to ASCII transliteration
- [ebooklib](https://github.com/aerkalov/ebooklib) - For EPUB file handling

## Troubleshooting

### Common Issues

**Issue**: "Failed to read EPUB file"
- **Solution**: Make sure the input file is a valid EPUB file. Try opening it in an EPUB reader first.

**Issue**: "Input file not found"
- **Solution**: Check that the file path is correct and the file exists.

**Issue**: Output EPUB is corrupted
- **Solution**: This is rare but can happen with complex EPUBs. Try using an EPUB validator on the input file first.

## Use Cases

- 📖 Preparing ebooks for old Kindle devices (pre-2014 models)
- 🔤 Converting foreign language ebooks to ASCII-only for better compatibility
- 📱 Ensuring ebook compatibility across different devices and readers
- 🛠️ Batch processing ebook libraries for standardization

## Limitations

- The tool converts all Unicode to ASCII, which means some characters may lose their original meaning or appearance
- Special characters and symbols will be transliterated to their closest ASCII equivalents
- Some formatting or styling that relies on Unicode characters may be affected
- Metadata conversion may not work perfectly in all EPUB variants

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/eliottness/unidecode-epub).

