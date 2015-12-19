# -*- coding: utf-8 -*-
#import uuid, json, os, time
import uuid, os, time
from django.utils import simplejson as json
#from django.utils import simplejson as json
#from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.http import HttpResponse
#import Http404, settings
import settings
from django.http import Http404


def flash_upload_img(request):
	"Ueditor上传图片的flash处理函数"
	#不允许非post请求 
	if request.method <> 'POST':
		raise Http404
	now = time.localtime(time.time())
	ret = {'url':'', 'title':'', 'state':'Error'}
	#百度ueditor的flash上传插件要求返回的格式
	try:
		#django保存图片都是在request.FILES
		image = request.FILES.values()[0]
		if image.content_type in ('application/octet-stream','image/png','image/x-png','image/jpeg','image/pjpeg','image/gif','image/bmp'):
			#'application/octet-stream' flash是续传的，所以是这个格式
			ext = os.path.splitext(image.name)[-1] #获取后缀名
			name = unicode(uuid.uuid1())+ext #生成随机文件名
			url = 'uploadimg/'+time.strftime('%Y', now)+'/'+time.strftime('%m', now)+'/';
			file = os.path.join(settings.MEDIA_ROOT, url).replace('\\','/') #图片储取的目录，还记得MEDIA_ROOT吗?
			file = os.path.realpath( file )+'/'
			if not os.path.isdir(file):
				os.makedirs(file)
			file = file+name
			w = open(file, 'wb+')
			for chunk in image.chunks(): #每一个上传文件都是UploadFile对象
				w.write(chunk)
			w.close()
			try:
				os.chmod(file, 0644) #重要，更改文件的权限，不然有的系统给的是0777
			except:
				pass
			ret = {'url':settings.MEDIA_URL+url+name, 'title':name, 'state':'SUCCESS'}
	except:
		pass
	return HttpResponse( json.dumps(ret) ) #结果回传给falsh，让它可以在前端加载图片.

def isNumeric(str):
	"出入数据是否为数字类型"
	try:
		if int(str)<0:
			pass
		if int(str)==0:
			pass
		if int(str)>0:
			pass
		return True
	except:
		return False


import re
class IgnoreCrsfMiddleware(object):		#忽略！~
	
	def process_request(self, request, **karg):
	#对/flashUploadImg/ 这个URL屏蔽django的csrf
		if re.match(r'^/flashUploadImg/?$', request.path): 
			request.csrf_processing_done = True  #让其它组件不要再进行csrf检测了
			return None