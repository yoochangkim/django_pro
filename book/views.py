from django.shortcuts import render, redirect
from .models import Book
from django.utils import timezone
from django.core.paginator import Paginator
# Create your views here.


def delete(request,bpk):
    b=Book.objects.get(id=bpk)
    b.delete()
    return redirect("book:index")

def create(request):
    if request.method == "POST" :
        sn = request.POST.get("sname")
        su = request.POST.get("surl")
        sc = request.POST.get("scon")
        im = request.POST.get("impo")
        if sn and su and sc:
            if im:
                imp = True
            else:
                imp = False
            Book(site_name=sn, site_url=su, content=sc, user=request.user, impo=imp, pubdate=timezone.now()).save()
        return redirect("book:index")
    return render(request, "book/create.html")

def index(request):
    pg = request.GET.get("page",1)
    b = request.user.book_set.order_by('-pubdate')
    pag = Paginator(b, 6)
    obj = pag.get_page(pg)
    context={
        'blist' : obj
    }
    return render(request, "book/index.html", context)