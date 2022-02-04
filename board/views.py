from django.shortcuts import render, redirect
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages

# Create your views here.

def unlikey (request, bpk) :
    b = Board.objects.get(id=bpk)
    u = request.user
    if u in b.likey.all():
        b.likey.remove(u)
    return redirect("board:detail", bpk)

def likey(request, bpk) :
    b = Board.objects.get(id=bpk)
    b.likey.add(request.user)
    return redirect ("board:detail", bpk)

def update(request, bpk) : 
    b = Board.objects.get(id=bpk)
    
    if b.writer != request.user:
        messages.warning(request, "!! 접근이 잘못되었습니다")
        return redirect("board:index")
    
    if request.method == "POST" :
        s = request.POST.get("sub")
        c = request.POST.get("con")
        b.subject = s
        b.content = c
        b.save()
        return redirect("board:detail", bpk)
    
    context = { 
        "b" : b
    }
    return render(request, "board/update.html", context)

def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        Board(subject=s, writer=request.user, content=c, pubdate=timezone.now()).save()
        return redirect("board:index")
    return render(request, "board/create.html")

def delete(request, bpk) :
    b = Board.objects.get(id=bpk)
    if b.writer == request.user:
        b.delete()
    else:
        messages.warning(request, "!! 접근이 잘못되었습니다")
    return redirect("board:index")

def dreply(request, bpk, rpk) :
    r= Reply.objects.get(id=rpk)
    if r.replyer == request.user:
        r.delete()
    else:
        messages.warning(request, "!! 접근이 잘못되었습니다")
    return redirect("board:detail", bpk)

def creply(request, bpk) :
    b = Board.objects.get(id=bpk)
    co = request.POST.get("comm")
    Reply(b=b, replyer=request.user, comment=co, pubdate=timezone.now()).save()
    return redirect("board:detail",bpk)

def detail(request, bpk) :
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        "b" : b,
        "rlist" : r
    }
    return render(request, "board/detail.html", context)

def index(request) : 
    pg = request.GET.get("page",1)
    cate = request.GET.get("cate","")
    kw = request.GET.get("kw","")
    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            from acc.models import User
            try:
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b= Board.objects.none()
        else:
            b = Board.objects.filter(content__contains=kw)
    else:
        b = Board.objects.all()
    pag = Paginator(b, 10)
    obj = pag.get_page(pg)
    context = {
        'blist' : obj,
        'cate' : cate,
        'kw' : kw
    }
    return render(request, "board/index.html", context)





