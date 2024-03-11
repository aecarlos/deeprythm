import PyPDF2
from pdf2image import convert_from_path
import cv2

def crop_pdf(input_pdf, output_pdf, x0, y0, x1, y1):
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        page = reader.pages[0]

        # Get the original page dimensions
        page_width = float(page.mediabox.upper_right[0])
        page_height = float(page.mediabox.upper_right[1])

        # Calculate the coordinates of the cropped area
        x0 = x0 * page_width
        y0 = y0 * page_height
        x1 = x1 * page_width
        y1 = y1 * page_height

        # Crop the page
        page.mediabox.lower_left = (x0, y0)
        page.mediabox.upper_right = (x1, y1)

        # Write the cropped page to a new PDF
        writer = PyPDF2.PdfWriter()
        writer.add_page(page)

        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

def output_ecgs(input_pdf, crop_areas):
    for i, area in enumerate(crop_areas):
        output_pdf = f'ecg{i + 1}.pdf'
        crop_pdf(input_pdf, output_pdf, *area)


def convert_to_images(pdf_path, output_name):
        image = convert_from_path(pdf_path)
        image[0].save(output_name, 'JPEG')

def remove_grid(image_path, output_name):
    # Load the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding to binarize the image
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Perform morphological operations to remove gridlines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # Invert the colors
    inverted = cv2.bitwise_not(morph)

    cv2.imwrite(output_name, inverted)
