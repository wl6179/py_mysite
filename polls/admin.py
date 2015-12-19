# -*- coding: utf-8 -*-
from django.contrib import admin
from mysite.polls.models import Poll, Choice



#自定义管理表格
#定义集成——这段代码会告诉 Django：Choice 对象要直接在 Poll 管理页面下编辑。默认，提供 3 个多余选项。
class ChoiceInline(admin.TabularInline):#StackedInline\TabularInline
    model = Choice
    extra = 3
class PollAdmin(admin.ModelAdmin):
    list_display = ( 'question', 'pub_date' )
    #fields = ['pub_date', 'question']		#会与下边的fieldsets设定相互冲突！！！也许是因为他们都定义了顺序，所以冲突~
    fieldsets = [
        (None,               {'fields': ['question']}),
        ('投票发布日期',     {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]#---------<<<<<<<<<<<-----------------------

#class ChoiceAdmin(admin.ModelAdmin):
#    list_display = ( 'choice', 'votes' )
#    fields = ['poll', 'choice', 'votes']

admin.site.register( Poll, PollAdmin )
#admin.site.register( Choice, ChoiceAdmin )




























