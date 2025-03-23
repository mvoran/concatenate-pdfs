#!/usr/bin/env python3
"""Command-line interface for PDF concatenation tool."""

import sys
import argparse
from pathlib import Path

from .core import concatenate_pdfs

def main():
    """Entry point for the command-line interface."""
    parser = argparse.ArgumentParser(
        description="Concatenate PDF and JPEG files into a single PDF with slip sheets."
    )
    parser.add_argument("-o", "--output", required=True,
                        help="Output file name for the combined PDF (e.g., 'Supporting Documents.pdf')")
    parser.add_argument("-i", "--input", default=".",
                        help="Input directory containing files to concatenate (default: current directory)")
    parser.add_argument("--outdir",
                        help="Directory to save the combined PDF (defaults to input directory)")
    args = parser.parse_args()

    input_dir = Path(args.input).resolve()
    output_dir = Path(args.outdir if args.outdir is not None else args.input).resolve()
    
    # Add .pdf extension only if no extension exists
    output_filename = args.output if Path(args.output).suffix else args.output + '.pdf'
    output_file = output_dir / output_filename

    # Get title from output filename (without extension)
    title = Path(output_filename).stem

    if concatenate_pdfs(input_dir, output_file, title):
        print(f"Combined PDF saved as: {output_file}")
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main()) 