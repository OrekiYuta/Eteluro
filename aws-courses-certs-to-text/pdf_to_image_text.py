import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import os

# Directory settings
INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR/tesseract.exe'

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)


def pdf_to_images(pdf_path, output_folder):
    """
    Convert PDF to images and save them as PNG files in the specified output folder.

    Args:
    - pdf_path (str): Path to the input PDF file.
    - output_folder (str): Path to the folder where images will be saved.

    Returns:
    - image_paths (list): List of paths to the saved PNG images.
    """
    doc = fitz.open(pdf_path)
    image_paths = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        img_path = os.path.join(output_folder, f'page_{page_num + 1}.png')
        pix.save(img_path)
        image_paths.append(img_path)

    return image_paths


def ocr_images(image_paths, output_folder):
    """
    Perform OCR on the provided images and save the recognized text as .txt files.

    Args:
    - image_paths (list): List of paths to the input images.
    - output_folder (str): Path to the folder where text files will be saved.
    """
    for i, img_path in enumerate(image_paths):
        text = pytesseract.image_to_string(Image.open(img_path), lang='eng')  # Use 'chi_sim' for Chinese
        text_path = os.path.join(output_folder, f'page_{i + 1}.txt')
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text)


def main():
    """
    Main function to process all PDF files in the input folder.
    For each PDF file, convert it to images and extract text using OCR.
    The results are saved in separate folders within the output directory.
    """
    # Get a list of all PDF files in the input folder
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print("❌ No PDF files found in the input folder.")
        return

    for pdf_file in pdf_files:
        pdf_path = os.path.join(INPUT_DIR, pdf_file)
        pdf_name = os.path.splitext(pdf_file)[0]  # Get the filename without extension
        output_folder = os.path.join(OUTPUT_DIR, pdf_name)

        # Create a folder for each PDF file inside the output directory
        os.makedirs(output_folder, exist_ok=True)

        print(f"📄 Processing file: {pdf_path}")

        image_paths = pdf_to_images(pdf_path, output_folder)
        ocr_images(image_paths, output_folder)

        print(f"✅ Done! PNG and text files have been saved in the {output_folder} folder.")


if __name__ == '__main__':
    main()
