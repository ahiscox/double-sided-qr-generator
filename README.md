# Double-Sided QR Generator

A Python tool that generates double-sided printable QR code sheets with unique UUIDs. Perfect for inventory tracking, asset management, or any application requiring two-sided QR codes. Features automatic alignment for double-sided printing, light cutting guides, and high error correction for reliable scanning.

## Features

- Generates unique QR codes with UUIDs
- Creates double-sided printable sheets
- QR codes are properly aligned for double-sided printing
- Light gray cutting guides
- Configurable number of pages
- High error correction for reliable scanning
- Centered layout with proper margins
- Black and white QR codes for maximum contrast

## Requirements

- Python 3.6 or higher
- Required packages:
  - qrcode
  - reportlab
  - Pillow

## Installation

### Using Pixi (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd double-sided-qr-generator
```

2. Install dependencies using Pixi:
```bash
pixi install
```

### Using pip (Alternative)

1. Clone the repository:
```bash
git clone <repository-url>
cd double-sided-qr-generator
```

2. Install dependencies using pip:
```bash
pip install -r requirements.txt
```

> **Note:** While pip installation should work, it has not been tested. The Pixi installation method is the recommended and tested approach.

## Usage

Run the script to generate QR code sheets:

```bash
# Using Pixi
pixi run generate --pages 1 --output /path/to/output.pdf

# Using pip
python generate.py --pages 1 --output /path/to/output.pdf
```

The script will generate a PDF file at the specified location. If no output path is provided, it will create `qr_codes.pdf` in the current directory. Each page set consists of two pages - a front page with QR codes and a back page with corresponding numbers.

### Command Line Arguments

- `--pages`: Number of page sets to generate (each set is 2 pages). Default is 1.
- `--output`: Path where the PDF should be saved. Optional, defaults to `qr_codes.pdf` in current directory.

### Python Module Usage

You can also use the generator in your own Python scripts:

```python
from generate import generate_qr_sheets

# Generate 3 sets of pages (6 pages total) to a specific location
generate_qr_sheets(num_pages=3, output_path="/path/to/output.pdf")
```

## How it Works

The script `generate.py`