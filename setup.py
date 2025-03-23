"""Setup configuration for pdf_concatenator package."""

from setuptools import setup, find_packages

setup(
    name="pdf_concatenator",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyPDF2>=3.0.0",
        "reportlab>=4.0.0",
        "Pillow>=10.0.0",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "pdfconcat=pdf_concatenator.__main__:main",
        ],
    },
    author="Michael Voran",
    author_email="mbvoran@gmail.com",
    description="A tool for concatenating PDFs and JPEGs with slip sheets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mbvoran/concatenate-pdfs",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
) 