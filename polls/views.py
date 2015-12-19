# -*- coding: utf-8 -*-
# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from mysite.polls.models import Poll

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    t = loader.get_template('polls/index.html')
    c = Context({
        'latest_poll_list': latest_poll_list,
    })
    return HttpResponse(t.render(c))


#from django.http import Http404
## ...
#def detail(request, poll_id):
#    try:
#        p = Poll.objects.get(pk=poll_id)
#    except Poll.DoesNotExist:
#        raise Http404
#    return render_to_response('polls/detail.html', {'poll': p})
#快捷：get_object_or_404()
#使用 get_object_or_404() 快捷，可以修改 detail() View，
from django.shortcuts import render_to_response, get_object_or_404
# ...
def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)#get_object_or_404直接就取代了object的数据库对象查询！
    return render_to_response('polls/detail.html', {'poll': p})
#这个 get_object_or_404() 函数用模型名称作为第一个参数，用主键数字作为另一个参数。 



from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from mysite.polls.models import Choice, Poll
# ...
def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)#提交错误变量时（有错误时）所传递的讯息~~~
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render_to_response('polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('mysite.polls.views.results', args=(p.id,)))#根据我的 URLconf 设置，reverse() 大概会返回字符串：'/polls/3/results/'……（有一点利用视图即URLconf设置，反向获取URL的意思~）。注意，你需要使用 View 的全称（包括前缀'mysite.polls.views.results'）。




def results(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/results.html', {'poll': p})