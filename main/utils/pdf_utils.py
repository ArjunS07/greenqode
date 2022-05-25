from fpdf import FPDF  # fpdf class
import qrcode, math
from pyrebase import pyrebase
from django.core.files.temp import NamedTemporaryFile

class PDF(FPDF):
    pass

def roundup(inp):
    return int(math.ceil(inp))

from main.models import Community, CommunityItem

# Constants
pdf_w=210
pdf_h=297
square_qr_side = 70
qr_label = 15
qr_padding = 5
leftmost_x = 30
topmost_y = 25
qrs_per_row = 2
rows_per_page = 3
qrs_per_page = qrs_per_row * rows_per_page

def generate_pdf_from_community_id(community_id, viewItem_absoluteURI):

    communnity = Community.objects.get(nameID=community_id)
    items = CommunityItem.objects.filter(community=communnity)

    urls_to_encode = []
    labels = []

    for item in items:
        print("absolute URI", viewItem_absoluteURI)
        item_url = viewItem_absoluteURI + "/" + communnity.nameID + '/' + item.item_id

        for _ in range(item.quantity):
            urls_to_encode.append(item_url)
            labels.append(item.name)

    pdf = PDF(orientation='P', unit='mm', format='A4')#pdf object
    pdf.set_font('Arial', '', 12)
    
    num_qrs = len(urls_to_encode)

    current_x = leftmost_x
    current_y = topmost_y

    num_pages_decimal = num_qrs / qrs_per_page
    num_pages = roundup(num_pages_decimal)

    num_qrs_used = 0
    current_qr_index = 0

    # Config

    for i in range(num_pages):

        pdf.add_page()

        remaining = num_qrs - num_qrs_used
        num_rows = 0
        if remaining > qrs_per_page:
            num_rows = rows_per_page
        else:
            num_rows = roundup(remaining / qrs_per_row)
        
        # reset y to 0
        current_y = topmost_y
        
        # For every row
        for j in range(num_rows):
            
            # Reset at beginning of every row        
            current_x = leftmost_x
            
            remaining = (num_qrs-num_qrs_used)
            num_items_in_row = 0
            
            if remaining >= qrs_per_row:
                num_items_in_row = qrs_per_row
            else:
                num_items_in_row = remaining % qrs_per_row
            
            for k in range(num_items_in_row):

                qr_temp_file = NamedTemporaryFile(delete=True)
                qr_image = qrcode.make(urls_to_encode[current_qr_index])

                qr_image_temp_path = qr_temp_file.name + '.png'
                qr_image.save(qr_image_temp_path)                

                # Add image
                pdf.image(qr_image_temp_path, current_x, current_y, square_qr_side, square_qr_side)
                
                # Draw cutting line above image
                pdf.dashed_line(current_x, current_y, current_x + square_qr_side + qr_padding, current_y)
                # Draw cutting line below image
                pdf.dashed_line(current_x, current_y + square_qr_side, current_x + square_qr_side + qr_padding, current_y + square_qr_side)
                
                # Draw cutting line to the left of the image
                pdf.dashed_line(current_x, current_y, current_x, current_y + square_qr_side + qr_padding * 2)
                # Draw cutting line to the right of the image
                pdf.dashed_line(current_x + square_qr_side + qr_padding, current_y, current_x + square_qr_side + qr_padding, current_y + square_qr_side + qr_padding * 2)
                
                    
                # Add text
                pdf.text(current_x + qr_padding, current_y + square_qr_side + qr_padding + 1, labels[current_qr_index])
                
                # Draw line below text. Redundant if not above the last row
                pdf.dashed_line(current_x, current_y + square_qr_side + qr_padding * 2, current_x + square_qr_side + qr_padding, current_y + square_qr_side + qr_padding * 2)
    

                # Move ahead
                current_x += square_qr_side + qr_padding

                # No need to change y since this is the same row          
                
                        
                current_qr_index += 1
                num_qrs_used += 1
            
        
            # Advance y position
            current_y += square_qr_side + (qr_padding * 2)
    return pdf
