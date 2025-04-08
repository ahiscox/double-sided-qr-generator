from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import black, Color
import qrcode
import io
import os
import tempfile
import uuid
import argparse
from PIL import Image
import coolname
import hashlib
import random

# Create a light gray color (80% white, 20% black)
light_gray = Color(0.8, 0.8, 0.8)

def load_word_list():
    """Load words from wordlist.txt and split them into adjectives and nouns."""
    with open('wordlist.txt', 'r') as f:
        words = [line.strip() for line in f if line.strip()]
    
    # Split words into adjectives and nouns (simple heuristic)
    adjectives = [word for word in words if len(word) > 3 and not word.endswith('s')]
    nouns = [word for word in words if len(word) > 3 and word.endswith('s')]
    
    # Add some non-plural nouns
    nouns.extend([word for word in words if len(word) > 3 and not word.endswith('s')][:1000])
    
    return adjectives[:2000], nouns[:2000]  # Limit to 2000 words each for memory efficiency

# Load word lists at module level
ADJECTIVES, NOUNS = load_word_list()

def generate_qr_code(uuid_str):
    """Generate a QR code with high error correction."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(uuid_str)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def generate_name_from_uuid(uuid_str):
    """Generate a human-readable name from a UUID string."""
    # Convert UUID to a number to use for deterministic selection
    uuid_int = int(uuid_str.replace('-', ''), 16)
    
    # Create a custom configuration for 2-word names
    config = {
        'all': {
            'type': 'cartesian',
            'lists': ['adjective', 'noun']
        },
        'adjective': {
            'type': 'words',
            'words': ADJECTIVES
        },
        'noun': {
            'type': 'words',
            'words': NOUNS
        }
    }
    
    # Create a generator with our custom config
    generator = coolname.RandomGenerator(config)
    
    # Use the UUID to seed the random number generator
    random.seed(uuid_int)
    
    # Generate the name
    return generator.generate_slug()

def draw_page(c, uuids, rows, cols, start_x, start_y, cell_size, temp_dir, page_set, is_back_page=False):
    """Draw a page of QR codes, optionally flipped for the back page."""
    # Draw grid and place QR codes
    for i in range(rows):
        for j in range(cols):
            # Calculate position based on whether it's the back page
            if is_back_page:
                # For back page, reverse the column order
                col_idx = cols - 1 - j
                row_idx = i
            else:
                col_idx = j
                row_idx = i
            
            idx = row_idx * cols + col_idx
            uuid_str = uuids[idx]
            
            # Calculate cell position
            x = start_x + j * cell_size
            y = start_y + (rows - 1 - i) * cell_size
            
            # Draw cell border with light gray color
            c.setStrokeColor(light_gray)
            c.rect(x, y, cell_size, cell_size)
            
            # Generate QR code
            qr_img = generate_qr_code(uuid_str)
            
            # Save QR code to temporary file with unique name for this page set
            temp_file_path = os.path.join(temp_dir, f"qr_{page_set}_{idx}.png")
            qr_img.save(temp_file_path)
            
            # Calculate QR code position with 10px margin and vertical offset
            qr_margin = 10
            qr_size = cell_size - (2 * qr_margin)
            qr_x = x + qr_margin
            qr_y = y + qr_margin + (cell_size - qr_size) * 0.3  # Move up by 30% of remaining space
            
            # Draw QR code
            c.drawImage(temp_file_path, qr_x, qr_y, width=qr_size, height=qr_size)
            
            # Generate and draw human-readable name
            name = generate_name_from_uuid(uuid_str)
            c.setFont("Helvetica", 8)
            text_width = c.stringWidth(name, "Helvetica", 8)
            text_x = x + (cell_size - text_width) / 2
            text_y = qr_y - 2  # Position text relative to QR code position
            c.drawString(text_x, text_y, name)

def generate_qr_sheets(num_pages=1, output_path=None):
    """Generate a PDF containing double-sided QR code sheets.
    
    Args:
        num_pages (int): Number of page sets to generate (each set is 2 pages - front and back)
        output_path (str, optional): Path where the PDF should be saved. If None, defaults to 'qr_codes.pdf' in current directory.
    """
    # PDF dimensions
    page_width, page_height = letter
    margin = 0.5 * inch
    cols = 4  # Fixed number of columns
    
    # Calculate cell size to fit 4 columns with margins
    available_width = page_width - 2 * margin
    cell_size = available_width / cols
    
    # Calculate number of rows that will fit
    rows = int((page_height - 2 * margin) // cell_size)
    
    # Calculate total grid width and height
    total_grid_width = cols * cell_size
    total_grid_height = rows * cell_size
    
    # Calculate starting position to center the grid
    start_x = (page_width - total_grid_width) / 2
    start_y = (page_height - total_grid_height) / 2
    
    # Set default output path if none provided
    if output_path is None:
        output_path = "qr_codes.pdf"
    
    # Create PDF with absolute path
    output_path = os.path.abspath(output_path)
    c = canvas.Canvas(output_path, pagesize=letter)
    
    # Create temporary directory for QR code images
    temp_dir = tempfile.mkdtemp()
    
    try:
        for page_set in range(num_pages):
            # Generate unique UUIDs for each QR code in this set
            uuids = [str(uuid.uuid4()) for _ in range(rows * cols)]
            
            # Draw first page of the set
            draw_page(c, uuids, rows, cols, start_x, start_y, cell_size, temp_dir, page_set)
            
            # # Add page dimensions and grid info to first page
            # c.setFont("Helvetica", 10)
            # c.drawString(50, 50, f"Page: {page_width/inch:.1f} x {page_height/inch:.1f} inches")
            # c.drawString(50, 35, f"Grid: {cols} columns x {rows} rows")
            # c.drawString(50, 20, f"Cell size: {cell_size/inch:.2f} inches")
            # c.drawString(50, 5, f"Set {page_set + 1} of {num_pages}")
            
            # Start second page
            c.showPage()
            
            # Draw second page (flipped)
            draw_page(c, uuids, rows, cols, start_x, start_y, cell_size, temp_dir, page_set, is_back_page=True)
            
            # # Add page dimensions and grid info to second page
            # c.setFont("Helvetica", 10)
            # c.drawString(50, 50, f"Page: {page_width/inch:.1f} x {page_height/inch:.1f} inches")
            # c.drawString(50, 35, f"Grid: {cols} columns x {rows} rows")
            # c.drawString(50, 20, f"Cell size: {cell_size/inch:.2f} inches")
            # c.drawString(50, 5, f"Set {page_set + 1} of {num_pages}")
            
            # If this isn't the last set, start a new page
            if page_set < num_pages - 1:
                c.showPage()
        
        # Save the PDF
        c.save()
        print(f"PDF generated successfully at: {output_path}")
    
    finally:
        # Clean up temporary files
        for page_set in range(num_pages):
            for i in range(rows * cols):
                temp_file_path = os.path.join(temp_dir, f"qr_{page_set}_{i}.png")
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
        os.rmdir(temp_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate QR code sheets')
    parser.add_argument('--pages', type=int, default=1, help='Number of page sets to generate (each set is 2 pages)')
    parser.add_argument('--output', type=str, help='Path where the PDF should be saved (default: qr_codes.pdf)')
    args = parser.parse_args()
    
    generate_qr_sheets(args.pages, args.output) 