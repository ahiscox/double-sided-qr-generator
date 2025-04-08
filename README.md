# QR Code Generator

A Python tool for generating sheets of QR codes with unique UUIDs, optimized for double-sided printing and cutting.

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
- Required packages (install via `pip install -r requirements.txt`):
  - qrcode
  - reportlab
  - Pillow

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd qrcode_generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line

Generate QR code sheets from the command line:

```bash
python layout_test.py --pages 3
```

This will generate 6 pages (3 sets of front/back pages) with unique QR codes on each set.

Arguments:
- `--pages`: Number of page sets to generate (each set is 2 pages). Default is 1.

### As a Python Module

You can also use the generator in your own Python scripts:

```python
from layout_test import create_layout_test

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
python layout_test.py --pages 3
```

This will create `qr_codes.pdf` with:
- Pages 1-2: First set of unique QR codes
- Pages 3-4: Second set of unique QR codes
- Pages 5-6: Third set of unique QR codes

Each set has its own unique QR codes, and the front/back pages are properly aligned for double-sided printing. 