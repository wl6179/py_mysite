# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url

#使用缓存机制.OK
from django.views.decorators.cache import cache_page

urlpatterns = patterns('mysite.polls.views',
    
    #( r'^foo/(\d{1,2})/$', cache_page( my_view, 60 * 1500 ) ),		#缓存成功！！！
#    (r'^polls/$', 							'mysite.polls.views.index'),
#    (r'^polls/(?P<poll_id>\d+)/$', 			'mysite.polls.views.detail'),
#    (r'^polls/(?P<poll_id>\d+)/results/$', 	'mysite.polls.views.results'),
#    (r'^polls/(?P<poll_id>\d+)/vote/$', 	'mysite.polls.views.vote'),
	
    #我们可以将 patterns() 的第一个参数设置为重复的前缀'mysite.polls.views'，例如：
#    (r'^$', 'index'),
#    (r'^(?P<poll_id>\d+)/$', 'detail'),
#    (r'^(?P<poll_id>\d+)/results/$', 'results'),
#    (r'^(?P<poll_id>\d+)/vote/$', 'vote'),
    #注意：删除 "polls/"了！！！
)
#备注及要求、约定：
#1.使用命名的正则表达式组（命名组）形式，语法是 (?P<name>pattern)。例：(r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_archive),
#2.注意：如果在URLconf中使用命名组，那么命名组和非命名组是不能同时存在于同一个URLconf的模式中的。 如果你这样做，Django不会抛出任何错误，但你可能会发现你的URL并没有像你预想的那样匹配正确。（又是一个暗影芭比！！！！~~~~）
#3.要用通用视图：请参考笔记中最底部；再看DjangoBook2.0的第十一章内容；