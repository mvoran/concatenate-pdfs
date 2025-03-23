# PDF Concatenation Tool

A command-line tool that combines multiple PDF and JPEG files into a single PDF document, with automatically generated slip sheets for each file.

## Features

- Combines multiple PDF and JPEG files into a single PDF
- Automatically creates slip sheets with file names
- Maintains alphabetical order of files
- Supports both PDF and JPEG input formats
- Creates a title page with the output filename

## Sample Output

A sample output file is included in the repository as `Sample Output.pdf`. This demonstrates:
- The title page format
- How slip sheets appear between documents
- The overall document structure and formatting
- The quality of JPEG to PDF conversion

## Project Structure

```
PDFConcatenationTool/
├── LICENSE                     # MIT License
├── README.md                  # This file
├── requirements.txt           # Direct dependencies
├── setup.py                   # Package installation configuration
├── src/
│   └── pdf_concatenator/     # Main package directory
│       ├── __init__.py       # Package initialization
│       ├── __main__.py       # Command-line interface
│       └── core.py           # Core PDF processing functionality
└── tests/                    # Test directory (for future tests)
```

## Requirements

- Python 3.10 or higher
- Dependencies:
  - PyPDF2 >= 3.0.0
  - reportlab >= 4.0.0
  - Pillow >= 10.0.0

## Installation

1. Clone this repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Create and activate a virtual environment:
```bash
python3 -m venv pdf_concat_env
source pdf_concat_env/bin/activate  # On Unix/macOS
# or
pdf_concat_env\Scripts\activate  # On Windows
```

3. Install the package in development mode:
```bash
pip install -e .
```

## Usage

After installation, you can use the tool in two ways:

1. Using the installed command:
```bash
pdfconcat -o output.pdf -i /path/to/files
```

2. Using Python's module syntax:
```bash
python -m pdf_concatenator -o output.pdf -i /path/to/files
```

Options:
- `-o, --output`: Output file name (required). If no file extension is provided, '.pdf' will be added automatically. If any extension exists, it will be used as-is
- `-i, --input`: Input directory containing files to concatenate (default: current directory)
- `--outdir`: Directory to save the combined PDF (defaults to input directory)

Examples:
```bash
# Basic usage - combine files from current directory
pdfconcat -o combined          # Will create combined.pdf

# Specify input and output directories
pdfconcat -i /path/to/source --outdir /path/to/destination -o report.pdf

# Using any extension (though .pdf is recommended)
pdfconcat -o report.doc       # Will create report.doc
```

## Notes

- Files are processed in alphabetical order
- Supported file formats: PDF, JPEG (.jpg, .jpeg)
- Each file gets its own slip sheet with the filename
- The output PDF starts with a title page using the output filename
- The tool will automatically add .pdf extension if no extension is provided
- If you specify an extension (any extension), it will be used as-is 