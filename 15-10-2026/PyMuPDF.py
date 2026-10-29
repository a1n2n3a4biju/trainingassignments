import fitz
doc = fitz.open("EY_Digital_PDF_Practice.pdf")
# print("Pages:", len(doc))

# page_text=doc[0].get_text()
# print(page_text)

# for page in doc:
#     print(page.get_text())

# for page in doc:
#     if "maintenance" in page.get_text():
#         print("Yes")
#         break
#     else:
#         print("No")


all_text = ""
for page in doc:
    all_text += page.get_text()
# print("Count of V303:",all_text.count("V303"))


with open("digital_pdf_text.txt", "w") as f:
    f.write(all_text)