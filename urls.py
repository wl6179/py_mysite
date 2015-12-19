# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from mysite.views import hello, my_homepage_view, current_datetime, my_view

#为了导入settings.MEDIA_ROOT 的上传文件目录配置.
import settings

#admin
from django.contrib import admin
admin.autodiscover()

#处理表单之所在视图文件.
from mysite.books import views as viewsII

#使用缓存机制.OK
from django.views.decorators.cache import cache_page



#处理Ueditor.
from mysite import functions




#测试区--------------------------------------------------------------------------
#from django.shortcuts import render_to_response
#from django.http import HttpResponse
#def debug(request):
#	return render_to_response('debug.html')
from django.template.loader import get_template
from django.http import HttpResponse
from django.template import Template, Context, RequestContext
def custom_proc(request):
	return {
		'app':			'Debug Test',
		'user':			request.user,
		'ip_address':	request.META['REMOTE_ADDR']
	}
#注意：不需要Csrf防御的方式~——展示查询结果，处理之前包含#符合POST表单Csrf防御的方式的表单后，似乎不用在带入Csrf防御体系就能展示页面了！！！即使用正常的render_to_response来使用模板~
def debug( request ):
	#要像search视图那样-生成有POST表单的页面——含有{% csrf_token %}调用的~（就得用上RequestContext！）：
	t = get_template( 'debug.html' )
	html = t.render( RequestContext( request, { 'messages':'I am search function!' }, processors=[custom_proc] ) )
	return HttpResponse( html )
#测试区--------------------------------------------------------------------------






# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    
    ( r'^$', 		my_homepage_view ),
    
    ( r'^hello/$', 	hello ),
    
    ( r'^time/$', 	current_datetime ),
    
    ( r'^admin/',	include( admin.site.urls ) ),
    
    #表单.（界面，套入模板展现）
    ( r'^search-form/$', viewsII.search_form ),
    
    #处理表单.（功能函数）
    ( r'^search/$', viewsII.search ),
    
    
    
    ( r'^foo/(\d{1,2})/$', cache_page( my_view, 60 * 1500 ) ),		#缓存成功！！！
    
    
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    
    #include()，polls，参照另一个 URLconf。注意这个正则表达式结尾没有 $ 符号，但保留 / 斜线。
    #当 Django 遇到匹配 URL 时，它会把截取匹配部分，把以后的部分都传递给 include 的 URLconf，做进一步处理。 
    ( r'^polls/', include('mysite.polls.urls') ),
    
    
    
    
    
    
    
    
    
    
    
    url(r"^media/(?P<path>.*)$", "django.views.static.serve", {"document_root": settings.MEDIA_ROOT,}),
    
    
    
    
    
    
    
    
    
    
    
    url(r'^debug/', debug),			#测试。
    url(r'^comments/', include('django.contrib.comments.urls')),			#点评插件~
    
    
    url(r'^flashUploadImg/$', functions.flash_upload_img),	#上传函数
    
    
)
#备注及要求、约定：
#1.使用命名的正则表达式组（命名组）形式，语法是 (?P<name>pattern)。例：(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_archive),
#2.注意：如果在URLconf中使用命名组，那么命名组和非命名组是不能同时存在于同一个URLconf的模式中的。 如果你这样做，Django不会抛出任何错误，但你可能会发现你的URL并没有像你预想的那样匹配正确。（又是一个暗影芭比！！！！~~~~）
#3.要用通用视图：请参考笔记中最底部；再看DjangoBook2.0的第十一章内容；

