# -*- coding: utf-8 -*-
from django.template.loader import get_template

from django.template import Template, Context
from django.http import HttpResponse
import datetime

def hello(request):
    return HttpResponse("Hello world")

def my_homepage_view(request):
    return HttpResponse("Hello HomePage!")

'''def current_datetime(request):
	now = datetime.datetime.now()
	#t = Template("<html><body>It is now {{ current_date }}.</body></html>")	#Template
	t = get_template('current_datetime.html')
	html = t.render(Context({'current_date': now}))
	return HttpResponse(html)
'''

from django.shortcuts import render_to_response
import datetime

def current_datetime(request):
	now = datetime.datetime.now()
	return render_to_response('current_datetime.html', {'current_date': now})





#@cache_page(60 * 15)
#缓存成功！！！
def my_view( request, numPlus ):
	now = datetime.datetime.now()
	return render_to_response('current_datetime.html', {'current_date': now, 'numPlus': numPlus})