import pytesseract
import re
from PIL import Image
from pdf2image import convert_from_path

def detect_name_region(pdf_path, region, dpi=80, threshold=180):
    """
    Extracts text and confidence from a selected region of the first page of a PDF.
    Returns: (suggested_name, raw_text, avg_confidence)
    """
    images = convert_from_path(pdf_path, dpi=dpi, first_page=1, last_page=1)
    image = images[0]

    name_crop = image.crop(region)
    gray = name_crop.convert('L')
    bw = gray.point(lambda x: 0 if x < threshold else 255, '1')

    ocr_data = pytesseract.image_to_data(bw, output_type=pytesseract.Output.DATAFRAME)
    ocr_data = ocr_data[ocr_data.conf != -1]
    raw_text = " ".join(ocr_data['text'].dropna().tolist())
    avg_conf = round(ocr_data['conf'].mean(), 1) if not ocr_data.empty else 0

    match = re.search(r'Name[:\s\-]*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})', raw_text)
    suggested_name = match.group(1).strip().replace(' ', '_') if match else ''

    return suggested_name, raw_text, avg_conf
