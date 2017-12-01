from django.shortcuts import render,redirect,HttpResponse
from blog import models
from datetime import datetime
# Create your views here.


user = {
    'admin':'admin'
}


def auth(func):
    def inner(request,*args,**kwargs):
        v = request.COOKIES.get('user')
        if not v:
            return redirect('/')
        return func(request,*args,**kwargs)
    return inner



def index(request):
    posts = models.Post.objects.all().order_by("-pub_time")
    # n = posts.first().id      #默认显示第一个
    # nid = request.GET.get('nid',n)
    nid = request.GET.get('nid')
    post = models.Post.objects.filter(id=nid).first()
    url = '/?nid=%s' % nid
    if request.COOKIES.get('user'):
        is_login = True
        res =  render(request,'index.html',{'posts':posts,'p':post,'is_login':is_login})
        res.set_cookie('url',url)
        return res
    res = render(request,'index.html',{'posts':posts,'p':post})
    res.set_cookie('url', url)
    return res


@auth
def kinde(request):
    if request.method == 'GET':
        return render(request,'kinde.html')
    elif request.method == 'POST':
        title = request.POST.get('title')
        profile = request.POST.get('profile')
        content = request.POST.get('content')
        models.Post.objects.create(title=title,profile=profile,content=content,pub_time=datetime.now())
        return redirect('/')

@auth
def edit_b(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        post = models.Post.objects.filter(id=nid).first()
        return render(request,'kinde.html',{'post':post})

    elif request.method == 'POST':
        nid = request.POST.get('nid')
        title = request.POST.get('title')
        profile = request.POST.get('profile')
        content = request.POST.get('content')
        models.Post.objects.filter(id=nid).update(title=title, profile=profile, content=content)
        url = '/?nid=%s' % nid
        return redirect(url)

@auth
def delete(request):
    nid = request.GET.get('nid')
    models.Post.objects.filter(id=nid).delete()
    return redirect('/')

def login(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        if u == user.get(u) and p == user[u]:
            url = request.COOKIES.get('url')
            print(url)
            res = redirect(url)
            res.set_cookie('user',u)
            return res
        else:
            return HttpResponse('密码错误')

def out(request):
    user = request.COOKIES.get('user')
    url = request.COOKIES.get('url')
    res = redirect(url)
    res.set_cookie('user',user,max_age=0)
    return res

