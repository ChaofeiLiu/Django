"""Mybolg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include,re_path,url
from first.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',index,name='index.html'),
    path(r'ueditor/',include('DjangoUeditor.urls')),# 添加DjangoUeditor的url
    re_path('^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$',serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),  # 解决静态文件加载失败问题

    path(r'my_tuijian-<int:bid>.html',my_tuijian,name = 'My_tuijian'), # 博主推荐页
    path(r'newest-<int:zid>.html', newest_show, name='Newest'),  # 最新文章详情页


    path('myself/',myself,name = 'myself'),  # 关于博主
    path(r'show-<int:bid>.html',blist,name='blist'), #文章分类之列表页

    path(r'reg/',reg,name = 'reg'), #注册
    path(r'bpb/',bpb,name= 'bpb'),#注册处理函数
    path(r'logout/',user_logout,name = 'user_logout'), #登出

    path(r'login/',user_login,name='uesr_login'),# 登录页
    path(r'login_/',user_login_,name='user_login_'),  # 登陆处理函数

    path(r'tag/<tag>',shwo_tags,name='show_tags'),  # 标签展示页

    url('ping/',ping_list,name='ping_list'), # 调用获取数据
    url('add_p/',add_ping,name='add_ping'),
]
