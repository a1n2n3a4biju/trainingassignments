import fitz
import pytesseract
from PIL import Image

doc = fitz.open("EY_Scanned_PDF_OCR_Practice.pdf")

page = doc[0]

pix = page.get_pixmap()
pix.save("scanned_page.png")
image = Image.open("scanned_page.png")
text = pytesseract.image_to_string(image)
# print(text)

# if "Forklift FL-17" in text:
#     print("Forklift FL-17 detected")


# print("Found 'injuries'",text.lower().count("injuries"),"times")

# for line in text.splitlines():
#     if "inspection" in line.lower():
#         print(line)

# with open("ocr_result.txt", "w") as f:
#    f.write(text)

# print("the word 'inspection' appears",text.lower().count("inspection"),"times")

for l in text.splitlines():
    if "loading bay" in l.lower():
        print(l)