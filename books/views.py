# -*- coding: utf-8 -*-
# Create your views here.
from django.template.loader import get_template
from django.template import Template, Context, RequestContext


from django.http import HttpResponse
from django.shortcuts import render_to_response
from mysite.books.models import Book



def custom_proc(request):
	"A context processor that provides 'app', 'user' and 'ip_address'."
	return {
		'app':			'My app',
		'user':			request.user,
		'ip_address':	request.META['REMOTE_ADDR']
	}
#def search_form(request):
#	return render_to_response( 'search_form.html', )

#符合POST表单Csrf防御的方式（动用RequestContext）~
#似乎专门要一个显示表单函数，没什么用~（不如整合到search中（即负责显示，又负责处理！！！））
#已经被废了！
def search_form( request ):
	t = get_template('search_form.html')
	html = t.render( RequestContext( request, {'abcddd': 'abc', 'error': False} ) )
	return HttpResponse(html)

#def search(request):
#	if 'q' in request.POST:
#		#print "Content‐Type: text/html\n"
#		#HttpResponse._headers = {'content-type': ( 'Content-Type', 'text/html; charset=utf-8' )}
#		
#		message = '<html><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/><head><title>Result~</title></head><body><h1>You searched for: %s</h1></body></html>' % request.POST['q']
#	else:
#		message = 'You submitted an empty form.'
#	return HttpResponse( message )			#直接返回u字符串了，

#注意：不需要Csrf防御的方式~——展示查询结果，处理之前包含#符合POST表单Csrf防御的方式的表单后，似乎不用在带入Csrf防御体系就能展示页面了！！！即使用正常的render_to_response来使用模板~
def search( request ):
	errors = []
	if 'q' in request.POST:			#如果传输了参数q；
		q = request.POST['q']
		if not q:					#如果传输了参数q为空；
			errors.append('Enter a search term.请输入关键字！')
		elif len(q) > 30:			#如果传输了参数q为大于30个字符串长度；
			errors.append('Please enter at most 30 characters.最多只能输入长度为30字符！')
		else:
			#正确时.
			q = request.POST['q']
			books = Book.objects.filter( title__icontains=q )
			return render_to_response( 'search_results.html', { 'books':books, 'query':q } )
			#终止跳出.
	#else:
	#return HttpResponse( 'Please submit a search term.' )
	#return render_to_response( 'search_form.html', { 'error': True } )
	#要像search视图那样-生成有POST表单的页面（有得用上RequestContext！）：
	#错误处理时or无参数时（未开始处理；仅表单页时）.
	t = get_template( 'search_form.html' )
	html = t.render( RequestContext( request, { 'errors':errors, 'messages':'I am search function!' }, processors=[custom_proc] ) )
	return HttpResponse( html )		#此时虽然看似def search_form的查询页面，实质上已经是查询结果页面了，只不过也调用同一个模板罢了~~~~
	#此时已经不再需要/search-form/页面了~~~~~~~直接被我们/search/取代了！！！！！！！！！！！！！！！！！！！！！！













	