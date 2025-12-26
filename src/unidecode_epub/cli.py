"""Command-line interface for unidecode-epub."""

import argparse
import sys
import os
from .processor import process_epub


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog='unidecode-epub',
        description='Convert Unicode text in EPUB files to ASCII for old Kindle devices',
        epilog='This tool processes EPUB files by converting all Unicode characters to their ASCII equivalents, making them compatible with old MOBI-only Amazon Kindles.'
    )
    
    parser.add_argument(
        'input',
        help='Path to the input EPUB file'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Path to the output EPUB file (default: <input>_ascii.epub)',
        default=None
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )
    
    args = parser.parse_args()
    
    try:
        output_path = process_epub(args.input, args.output)
        print(f"Successfully processed EPUB file.")
        print(f"Input:  {os.path.abspath(args.input)}")
        print(f"Output: {os.path.abspath(output_path)}")
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
