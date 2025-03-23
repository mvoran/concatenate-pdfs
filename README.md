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

## Requirements

- Python 3.6+
- Dependencies:
  - PyPDF2
  - reportlab
  - Pillow (PIL)

## Installation

1. Clone this repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Create a virtual environment and activate it:
```bash
python3 -m venv pdf_concat_env
source pdf_concat_env/bin/activate  # On Unix/macOS
# or
pdf_concat_env\Scripts\activate  # On Windows
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python ConcatenatePDFs.py -o output.pdf -i /path/to/files
```

Options:
- `-o, --output`: Output file name (required)
- `-i, --input`: Input directory containing files to concatenate (default: current directory)
- `--outdir`: Directory to save the combined PDF (defaults to input directory)

Example:
```bash
# Combine all PDFs and JPEGs from the current directory
python ConcatenatePDFs.py -o combined.pdf

# Combine files from a specific directory and save to another location
python ConcatenatePDFs.py -i /path/to/source --outdir /path/to/destination -o combined.pdf
```

## Notes

- Files are processed in alphabetical order
- Supported file formats: PDF, JPEG (.jpg, .jpeg)
- Each file gets its own slip sheet with the filename
- The output PDF starts with a title page using the output filename 