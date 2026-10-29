from pypdf import PdfReader
reader = PdfReader("EY_Digital_PDF_Practice.pdf")
# print("Pages:", len(reader.pages))

page1 = reader.pages[0].extract_text()
# print("Text from the first page:")
# print(page1)

page2 = reader.pages[1].extract_text()
# print("Text from the second page:")
# print(page2)
#
# for page in reader.pages:
#     print(page.extract_text())
#
pdf= page1 + page2
# if "NorthStar Maintenance" in pdf:
#     print("NorthStar Maintenance is present in pdf")
# else:
#     print("NorthStar Maintenance is not present in pdf")
#
# print("Number of times 'vendor' occurs:",pdf.lower().count("vendor"))

with open("pypdf_output.txt", "w") as f:
    f.write(pdf)


