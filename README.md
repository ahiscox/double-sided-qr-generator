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

### Command Line

Generate QR code sheets from the command line:

```bash
# Using Pixi
pixi run python generate.py --pages 3

# Using pip
python generate.py --pages 3
```

This will generate 6 pages (3 sets of front/back pages) with unique QR codes on each set.

Arguments:
- `--pages`: Number of page sets to generate (each set is 2 pages). Default is 1.

### As a Python Module

You can also use the generator in your own Python scripts:

```python
from generate import create_layout_test

# Generate 3 sets of pages (6 pages total)
create_layout_test(num_pages=3)
```

## Output

The script generates a PDF file named `qr_codes.pdf` with the following characteristics:

- 4 columns of QR codes per page
- QR codes sized to fit the page with proper margins
- Light gray cutting guides
- Each QR code contains a unique UUID
- Front and back pages are properly aligned for double-sided printing
- Each set of pages (front/back) has its own unique QR codes

## Layout Details

- Page size: Standard letter (8.5" x 11")
- Margins: 0.5 inches
- QR code size: Automatically calculated to fit 4 columns
- QR code margin: 10 pixels within each cell
- Error correction: High (H) for reliable scanning
- Border color: Light gray (RGB: 0.8, 0.8, 0.8)

## Double-Sided Printing

The QR codes are arranged so that when printed double-sided:
1. Each QR code on the back aligns with its corresponding front code
2. The back page is mirrored to ensure proper alignment
3. Scanning either side of a cut-out piece will yield the same UUID

## Example

```bash
# Generate 3 sets of pages (6 pages total)
pixi run python generate.py --pages 3
```

This will create `qr_codes.pdf` with:
- Pages 1-2: First set of unique QR codes
- Pages 3-4: Second set of unique QR codes
- Pages 5-6: Third set of unique QR codes

Each set has its own unique QR codes, and the front/back pages are properly aligned for double-sided printing. 