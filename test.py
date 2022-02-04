import pdfplumber

with pdfplumber.open("아뱅.pdf") as pdf:
    for i in range(len(pdf.pages)):
        print("="*20)
        print(i, "page")
        print("="*20)
        first_page = pdf.pages[i]
        print(first_page.extract_text())
