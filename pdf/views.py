from django.shortcuts import render
import pdfplumber
# Create your views here.

def index(request):
    context = {}
    if request.method == "POST":
        a= request.FILES.get("pdf")
        pdf = pdfplumber.open(a)
        text = ""
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            text += "\n" + "="*50 + f"\n{i+1} PAGE TEXT\n" + "="*50 + "\n"
            text += page.extract_text()
        pdf.close()
        context.update({
            "page": text
        })
    return render(request, "pdf/index.html", context)
