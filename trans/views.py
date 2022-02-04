from django.shortcuts import render
import googletrans
from googletrans import Translator
# Create your views here.

def index(request):
    context = {
        "ndict" : googletrans.LANGUAGES
    }
    if request.method == "POST":
        bef= request.POST.get("before")
        f = request.POST.get("from")
        t = request.POST.get("to")
        translator = Translator()
        trans1 = translator.translate(bef, src=f, dest=t)
        context.update({
            "aft" : trans1.text,
            "bef" : bef,
            "from" : trans1.src,
            "to" : trans1.dest
        })
    return render(request, "trans/index.html", context)
