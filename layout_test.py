from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import black
import qrcode
import io
import os
import tempfile
import uuid
import argparse
from PIL import Image

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
            
            # Draw cell border
            c.rect(x, y, cell_size, cell_size)
            
            # Generate QR code
            qr_img = generate_qr_code(uuid_str)
            
            # Save QR code to temporary file with unique name for this page set
            temp_file_path = os.path.join(temp_dir, f"qr_{page_set}_{idx}.png")
            qr_img.save(temp_file_path)
            
            # Calculate QR code position with 10px margin
            qr_margin = 10
            qr_size = cell_size - (2 * qr_margin)
            qr_x = x + qr_margin
            qr_y = y + qr_margin
            
            # Draw QR code
            c.drawImage(temp_file_path, qr_x, qr_y, width=qr_size, height=qr_size)

def create_layout_test(num_pages=1):
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
    
    # Create PDF with absolute path
    output_path = os.path.abspath("qr_codes.pdf")
    c = canvas.Canvas(output_path, pagesize=letter)
    
    # Create temporary directory for QR code images
    temp_dir = tempfile.mkdtemp()
    
    try:
        for page_set in range(num_pages):
            # Generate unique UUIDs for each QR code in this set
            uuids = [str(uuid.uuid4()) for _ in range(rows * cols)]
            
            # Draw first page of the set
            draw_page(c, uuids, rows, cols, start_x, start_y, cell_size, temp_dir, page_set)
            
            # Add page dimensions and grid info to first page
            c.setFont("Helvetica", 10)
            c.drawString(50, 50, f"Page: {page_width/inch:.1f} x {page_height/inch:.1f} inches")
            c.drawString(50, 35, f"Grid: {cols} columns x {rows} rows")
            c.drawString(50, 20, f"Cell size: {cell_size/inch:.2f} inches")
            c.drawString(50, 5, f"Set {page_set + 1} of {num_pages}")
            
            # Start second page
            c.showPage()
            
            # Draw second page (flipped)
            draw_page(c, uuids, rows, cols, start_x, start_y, cell_size, temp_dir, page_set, is_back_page=True)
            
            # Add page dimensions and grid info to second page
            c.setFont("Helvetica", 10)
            c.drawString(50, 50, f"Page: {page_width/inch:.1f} x {page_height/inch:.1f} inches")
            c.drawString(50, 35, f"Grid: {cols} columns x {rows} rows")
            c.drawString(50, 20, f"Cell size: {cell_size/inch:.2f} inches")
            c.drawString(50, 5, f"Set {page_set + 1} of {num_pages}")
            
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
    args = parser.parse_args()
    
    create_layout_test(args.pages) 