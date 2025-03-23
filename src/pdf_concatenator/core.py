"""Core functionality for PDF concatenation."""

import sys
import tempfile
import shutil
from pathlib import Path
from typing import Optional

from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

def create_slip_sheet(text: str, output_pdf_path: str) -> None:
    """
    Create a single-page PDF with the given text centered.
    Uses Helvetica-Bold 28pt as a proxy for Aptos Display.

    Args:
        text: The text to display on the slip sheet
        output_pdf_path: Path where the slip sheet PDF will be saved
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

def convert_to_pdf(input_file: Path, output_dir: Path) -> str | None:
    """
    Convert input file to PDF if needed.

    Args:
        input_file: Path to the input file
        output_dir: Directory to save converted PDF

    Returns:
        str | None: Path to the PDF file, or None if conversion failed
    """
    ext = input_file.suffix.lower()
    if ext == ".pdf":
        return str(input_file.resolve())
    elif ext in [".jpg", ".jpeg"]:
        try:
            image = Image.open(str(input_file))
            pdf_path = output_dir / (input_file.stem + ".pdf")
            if image.mode != "RGB":
                image = image.convert("RGB")
            image.save(str(pdf_path), "PDF", resolution=100.0)
            return str(pdf_path.resolve())
        except Exception as e:
            print(f"Error opening image {input_file.name}: {e}", file=sys.stderr)
            return None
    else:
        return None

def concatenate_pdfs(input_dir: Path, output_file: Path, title: str) -> bool:
    """
    Concatenate PDFs and images from input directory with slip sheets.

    Args:
        input_dir: Directory containing input files
        output_file: Path for the output PDF
        title: Title for the first slip sheet

    Returns:
        bool: True if successful, False otherwise
    """
    allowed_ext = {".pdf", ".jpg", ".jpeg"}
    files = [f for f in input_dir.iterdir() if f.is_file() and f.suffix.lower() in allowed_ext]
    files.sort(key=lambda x: x.name.lower())

    if not files:
        print("No PDF or JPEG files found in the input directory.")
        return False

    temp_dir = Path(tempfile.mkdtemp())
    try:
        converted_files = []
        for f in files:
            pdf_path = convert_to_pdf(f, temp_dir)
            if pdf_path is None:
                print(f"Skipping unsupported file: {f.name}")
                continue
            converted_files.append((f.name, pdf_path))

        if not converted_files:
            print("No files were successfully processed.")
            return False

        writer = PdfWriter()

        # Create and add title slip sheet
        slip_combined = temp_dir / "slip_combined.pdf"
        create_slip_sheet(title, str(slip_combined))
        combined_reader = PdfReader(str(slip_combined))
        for page in combined_reader.pages:
            writer.add_page(page)

        # Add each file with its slip sheet
        for orig_name, pdf_file in converted_files:
            slip_path = temp_dir / f"slip_{orig_name}.pdf"
            create_slip_sheet(Path(orig_name).stem, str(slip_path))
            
            # Add slip sheet
            slip_reader = PdfReader(str(slip_path))
            for page in slip_reader.pages:
                writer.add_page(page)
            
            # Add document
            file_reader = PdfReader(pdf_file)
            for page in file_reader.pages:
                writer.add_page(page)

        # Write the final PDF
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "wb") as f_out:
            writer.write(f_out)

        return True

    finally:
        shutil.rmtree(temp_dir) 