#!/usr/bin/env python3
import os
import sys
import argparse
import tempfile
import shutil
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

def create_slip_sheet(text, output_pdf_path):
    """
    Create a single-page PDF with the given text centered.
    Uses Helvetica-Bold 28pt as a proxy for Aptos Display.
    """
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 28)
    text_width = c.stringWidth(text, "Helvetica-Bold", 28)
    x = (width - text_width) / 2
    y = height / 2
    c.drawString(x, y, text)
    c.showPage()
    c.save()

def convert_to_pdf(input_file, output_dir):
    """
    If input_file is already a PDF, return its path.
    For JPEGs, convert using PIL.
    """
    ext = input_file.suffix.lower()
    if ext == ".pdf":
        return str(input_file.resolve())
    elif ext in [".jpg", ".jpeg"]:
        try:
            image = Image.open(str(input_file))
        except Exception as e:
            print(f"Error opening image {input_file.name}: {e}", file=sys.stderr)
            return None
        pdf_path = output_dir / (input_file.stem + ".pdf")
        if image.mode != "RGB":
            image = image.convert("RGB")
        image.save(str(pdf_path), "PDF", resolution=100.0)
        return str(pdf_path.resolve())
    else:
        # Unsupported file type (Word/Pages are excluded)
        return None

def main():
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

    # Allowed file extensions: PDF and JPEG
    allowed_ext = {".pdf", ".jpg", ".jpeg"}

    # Get all allowed files from the input directory
    files = [f for f in input_dir.iterdir() if f.is_file() and f.suffix.lower() in allowed_ext]
    files.sort(key=lambda x: x.name.lower())

    if not files:
        print("No PDF or JPEG files found in the input directory.")
        sys.exit(1)

    # Create a temporary directory for converted PDFs and slip sheets
    temp_dir = Path(tempfile.mkdtemp())
    converted_files = []

    # Convert or accept the files as PDFs
    for f in files:
        pdf_path = convert_to_pdf(f, temp_dir)
        if pdf_path is None:
            print(f"Skipping unsupported file: {f.name}")
            continue
        converted_files.append((f.name, pdf_path))

    if not converted_files:
        print("No files were successfully processed.")
        shutil.rmtree(temp_dir)
        sys.exit(1)

    writer = PdfWriter()

    # Create the initial slip sheet with the combined PDF title (without extension)
    combined_title = Path(args.output).stem
    slip_combined = temp_dir / "slip_combined.pdf"
    create_slip_sheet(combined_title, str(slip_combined))
    combined_reader = PdfReader(str(slip_combined))
    for page in combined_reader.pages:
        writer.add_page(page)

    # For each file, add a slip sheet followed by the file content
    for orig_name, pdf_file in converted_files:
        slip_path = temp_dir / f"slip_{orig_name}.pdf"
        title_text = Path(orig_name).stem  # File name in Title case (without extension)
        create_slip_sheet(title_text, str(slip_path))
        slip_reader = PdfReader(str(slip_path))
        for page in slip_reader.pages:
            writer.add_page(page)
        file_reader = PdfReader(pdf_file)
        for page in file_reader.pages:
            writer.add_page(page)

    # Write out the final combined PDF
    with open(output_file, "wb") as f_out:
        writer.write(f_out)

    print(f"Combined PDF saved as: {output_file}")

    # Cleanup temporary directory
    shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()