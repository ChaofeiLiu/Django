import json
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from first.models import *

# Create your views here.

# 调用获取数据
def ping_list(request):
    #把数据库的数据调出来并序列化成json，传到前端
    ping_data = {}
    models_data = djangojson()
    json_data = json.dumps(models_data)
    ping_data['json_data'] = json_data
    return HttpResponse(json_data)

class ShopcartSerializers2(serializers.ModelSerializer):
    class Meta:
        # model =Shopcart 获取所有表中数据，并序列化
        model = Ping # Article 可以更换数据库，此为接口
        fields = "__all__"  # 是否获取所有数据，也是接口
        depth = 1 #深度为1  (获取深度)

def djangojson():
    ping_list = Ping.objects.all().order_by("-id")  # 只获取两条数据
    serializer = ShopcartSerializers2(ping_list,many=True)  # 序列化
    return serializer.data  # 把数据传出去

def index(request):
    all_category =Category.objects.all() #分类表数据
    bbb =Banner.objects.filter(is_active=True)[:4]  # 轮播图数据
    my_tj = My_tuijian.objects.all()[:3] # 博主推荐
    rm =Article.objects.all().order_by('-views')[:10]  #点击量排行前十的文章
    tag = Tag.objects.all()[:6] #所有标签
    newest = Article.objects.all().order_by('-id')[:6] # 最新文章
    ttt = Article.objects.filter(tui_id=1)[:6] # 首页推荐
    cont = {}
    cont['all_category']= all_category
    cont['bbb']= bbb
    cont['my_tj'] = my_tj
    cont['rm'] = rm
    cont['tag'] =tag
    cont['newest'] =newest
    cont['ttt'] = ttt
    return render(request,'index.html',cont)

def my_tuijian(request,bid):
    bb = My_tuijian.objects.filter(id=bid)
    k = list(bb)[0]
    return render(request,k)

def newest_show(request,zid):
    show = Article.objects.get(id = zid)
    previous_blog = Article.objects.filter(create_time__gt=show.create_time,categroy=show.categroy.id).first()
    next_blog = Article.objects.filter(create_time__lt=show.create_time,categroy=show.categroy.id).last()
    show.views = show.views + 1
    show.save()
    return render(request,'read.html',locals())

def myself(request):
    return render(request,'myself.html')

def blist(request,bid):
    aa = Article.objects.filter(categroy_id=bid)
    cname =  Category.objects.get(id=bid)       #获取当前分类名
    # 分页
    list = aa
    page = request.GET.get('page')  # 在url中获取当前页数
    paginator = Paginator(list,2)   # 对查询到的数据对象list进行分页，设置超过5条数据就分页

    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果输入页码不是整数，显示第一页内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)      # 如果输入页数不在系统页码表，显示最后一页的内容
    return render(request,'blist.html',locals())

def reg(request):
    return render(request,'reg.html')

#注册登录
@csrf_exempt
def bpb(request):
    #接收参数
    bname =request.POST.get('user_name')
    bpwd = request.POST.get('pwd')
    bcpwd = request.POST.get('cpwd')
    beamil = request.POST.get('email')
    print(bname,bpwd,bcpwd,beamil)

    tuser = User.objects.create_user(username=bname,password=bpwd,email=beamil) #插入数据
    login(request,tuser) #登录
    return render(request,'tiao.html')

def user_logout(request):
    logout(request)
    return render(request,'tiao.html')

def user_login(request):
    return render(request,'login.html')

@csrf_exempt
def user_login_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passward = request.POST.get('pwd')
        print(username,passward)
        user = authenticate(username=username,password=passward)
        print(user)
        if user is not None:
            login(request,user)
            return redirect('/index/')
        return render(request,'login.html')

# 标签页展示
def shwo_tags(request,tag):
    list = Article.objects.filter(tags__name=tag)
    tag_name = Tag.objects.get(name=tag)

    # 分页
    page = request.GET.get('page')
    tags = Tag.objects.all()
    paginator = Paginator(list,2)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果输入页码不是整数，显示第一页内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)      # 如果输入页数不在系统页码表，显示最后一页的内容
    return render(request,'btags.html',locals())
@csrf_exempt
def add_ping(request):
    ping_boby= request.POST.get('pbody')
    article_id = request.POST.get('tid')
    user_id = request.POST.get('uid')
    print(ping_boby,article_id,user_id)
    if ping_boby =='':
        return render(request,'read.html')
    ping_data= Ping.objects.create(pbody=ping_boby,particle_id=article_id,user_id=user_id)
    ping_list(request) #把接口数据更新
    return render(request,'read.html')
