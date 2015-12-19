# -*- coding: utf-8 -*-
from django.contrib import admin
from mysite.news.models import Reporter, Article, Class_A



#自定义管理表格
class ArticleAdmin(admin.ModelAdmin):
    list_display 		= ( 'headline', 'reporter', 'cxbg_product_class', 'pub_date' )
    #fields = ['reporter', 'pub_date', 'headline', 'content']	#会与下边的fieldsets设定相互冲突！！！也许是因为他们都定义了顺序，所以冲突~
    fieldsets = [
        ( None,         { 'fields': [ 'reporter', 'cxbg_product_class' ] } ),
        ( '文章内容',   { 'fields': [ 'pub_date', 'headline', 'content' ], 'classes': [ 'collapse' ] } ),
    ]





admin.site.register(Reporter)
admin.site.register( Article, ArticleAdmin )

#admin.site.register(Class_A)

























