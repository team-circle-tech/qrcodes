import csv
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image, ImageDraw

# CSV file path
csv_file_path = "/path/to/yourfile.csv"
logo_path = "/path/to/yourfile.csv"

# Open the CSV file
with open(csv_file_path, "r", newline="") as csvfile:
    reader = csv.reader(csvfile)

    # Iterate over each row (skip the header row if present)
    for i, row in enumerate(reader):
        if i == 0 and row[0].lower() == 'base_url':  # Check if first row is header
            continue

        # Ensure sufficient data in the row (at least base URL)
        if len(row) < 1:
            print(f"Skipping invalid row {i+1}: Not enough data")
            continue

        # Build URL with parameters
        base_url = row[0]
        params = []

        # Iterate over parameters in steps of 2 to get name-value pairs
        for j in range(1, len(row), 2):
            # Check for missing value and skip or use a default
            if j + 1 >= len(row):
                print(f"Warning: Missing value for parameter '{row[j]}' in row {i+1}")
                continue
            params.append(f"{row[j]}={row[j+1]}")

        url = base_url + "?" + "&".join(params)

        # Create QR code with logo
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        #Load and resize logo
        logo = Image.open(logo_path)
        basewidth = 80 # adjust the size as needed
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
        
        # Create QR code image with style and logo
        qr_image = qr.make_image(
            image_factory=StyledPilImage, 
            module_drawer=RoundedModuleDrawer(),
            color_mask=SolidFillColorMask(front_color=(85, 98, 112), back_color=(248, 250, 252))
        )
        pos = ((qr_image.size[0] - logo.size[0]) // 2, (qr_image.size[1] - logo.size[1]) // 2)
        qr_image.paste(logo, pos)


        # Save as PNG
        param1_value = row[2] if len(row) > 1 else "qr_code"
        output_file = f"{param1_value}.png"  # Output as PNG

        # Save the QR code image
        qr_image.save(output_file)

        print(f"QR code saved as {output_file}")
