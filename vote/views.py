from django.shortcuts import render, redirect
from .models import Topic, Menu
# Create your views here.

def cancel(request, tpk):
    t=Topic.objects.get(id=tpk)
    u=request.user
    if u in t.voter.all():
        t.voter.remove(u)
        u.menu_set.get(sub=t).choicer.remove(u)
    return redirect("vote:detail", tpk)


def vote(request, tpk):
    t=Topic.objects.get(id=tpk)
    if not request.user in t.voter.all():
        t.voter.add(request.user)
        mpk = request.POST.get("menu")
        m = Menu.objects.get(id=mpk)
        m.choicer.add(request.user)
    return redirect("vote:detail", tpk)

def detail(request,tpk):
    t = Topic.objects.get(id=tpk)
    m = t.menu_set.all()
    context = {
        "t" : t,
        "mlist" : m
    }
    return render(request, "vote/detail.html", context)

def index(request):
    t = Topic.objects.all()
    context = {
        "tlist" : t
    }
    return render(request, "vote/index.html", context)