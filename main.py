import subprocess

import pyperclip

TEMP_DIR = "/tmp/"
SCREENSHOT_TEMP_FILENAME = TEMP_DIR + "SnapText-screenshot.png"
TESSERACT_TEMP_FILENAME = TEMP_DIR + "SnapText-tesseract"
TESSERACT_LANGUAGE = "eng"

SCREENSHOT_COMMAND = ["gnome-screenshot", "--area", "--file", SCREENSHOT_TEMP_FILENAME]
TESSERACT_COMMAND = [
    "tesseract",
    SCREENSHOT_TEMP_FILENAME,
    TESSERACT_TEMP_FILENAME,
    "-l",
    TESSERACT_LANGUAGE,
]

# Check if gnome-screenshot and tesseract are installed
try:
    subprocess.run(["gnome-screenshot", "--version"], stdout=subprocess.DEVNULL)
    subprocess.run(["tesseract", "--version"], stdout=subprocess.DEVNULL)
except FileNotFoundError as e:
    raise Exception(
        "gnome-screenshot or tesseract not found. Please install them."
    ) from e

# Take a screenshot
try:
    subprocess.run(SCREENSHOT_COMMAND, check=True)
except subprocess.CalledProcessError as e:
    print("Error taking screenshot")
    raise e

try:
    # Perform OCR on the image
    subprocess.run(TESSERACT_COMMAND, check=True)
except subprocess.CalledProcessError as e:
    print("Error extracting text from image")
    raise e

# Read the extracted text. Tesseract appends .txt to the output filename
with open(TESSERACT_TEMP_FILENAME + ".txt", "r") as f:
    extracted_text = f.read()

# Remove the last newline character
extracted_text = extracted_text.strip()

# Copy the extracted text to the clipboard
pyperclip.copy(extracted_text)

# Print the extracted text
print("Extracted Text:")
print(extracted_text)
