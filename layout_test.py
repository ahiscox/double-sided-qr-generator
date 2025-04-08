from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import black

def create_layout_test():
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
    
    # Create PDF
    c = canvas.Canvas("layout_test.pdf", pagesize=letter)
    
    # Draw grid
    for i in range(rows):
        for j in range(cols):
            # Calculate cell position
            x = start_x + j * cell_size
            y = start_y + (rows - 1 - i) * cell_size
            
            # Draw cell border
            c.rect(x, y, cell_size, cell_size)
            
            # Add cell coordinates for reference
            c.setFont("Helvetica", 8)
            c.drawString(x + 5, y + 5, f"({j},{i})")
    
    # Add page dimensions and grid info
    c.setFont("Helvetica", 10)
    c.drawString(50, 50, f"Page: {page_width/inch:.1f} x {page_height/inch:.1f} inches")
    c.drawString(50, 35, f"Grid: {cols} columns x {rows} rows")
    c.drawString(50, 20, f"Cell size: {cell_size/inch:.2f} inches")
    
    c.save()

if __name__ == "__main__":
    create_layout_test() 