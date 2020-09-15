from django.contrib import admin
from first.models import *
# Register your models here.

admin.site.site_header = '我的博客管理系统'
admin.site.site_title = '欢迎进入后台管理系统'
admin.site.index_title = '青城山博客'

admin.site.register(Article)
admin.site.register(Banner)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Tui)
admin.site.register(Link)
admin.site.register(My_tuijian)
admin.site.register(Ping)
