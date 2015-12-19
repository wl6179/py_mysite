# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.localflavor.us.models import USStateField


#from django.utils.translation import ugettext_lazy as _			#i18n




class Person(models.Model):
	first_name 		= models.CharField( max_length=50 )
	last_name 		= models.CharField( max_length=50 )
	birth_date 		= models.DateField()		#没有auto设定（默认值）的时间字段，所以可以手工填写！
	address 		= models.CharField( max_length=100 )
	city 			= models.CharField( max_length=50 )
	state 			= USStateField()			# Yes, this is U.S.‐centric...美国州下拉选择列表
	
	
	#定义下拉框列表字段choices.
	GENDER_CHOICES 	= (
		('M', 'Male'),
		('F', 'Female'),
		('Audio', (
	            ('vinyl', 'Vinyl'),
	            ('cd', 'CD'),
	        )
	    ),
	    ('Video', (
	            ('vhs', 'VHS Tape'),
	            ('dvd', 'DVD'),
	        )
	    ),
	)
	gender 			= models.CharField( max_length=1, choices=GENDER_CHOICES )
	
	#要新增字段，必须首先要把原表删除后，再运行python manage.py syncdb命令创建新表才行！！！
	#当对象第一次产生时字段设置为当前日期。一般用来产生对象的建立时间
	adddate			= models.DateTimeField( auto_now_add=True )
	#每次对象保存时，自动设置为当前日期。一般用来产生最后一次修改时间
	modifydate		= models.DateTimeField( auto_now=True )
	
	
	#测试多几个：
	Test_IPAddressField			= models.IPAddressField( default='0.0.0.0', help_text="注意: <em style='color:red'>打雷了，下雨了，收衣服啦！</em>." )
	Test_NullBooleanField		= models.NullBooleanField()
#	Test_PhoneNumberField		= models.PhoneNumberField()#我不知道外国的电话号码格式~~~先不试了~
	Test_PositiveIntegerField	= models.PositiveIntegerField()
	Test_SlugField				= models.SlugField()
	Test_TimeField				= models.TimeField()
	Test_TextField				= models.TextField()
	Test_XMLField				= models.XMLField()
	
#	Test_ImageField				= models.ImageField( upload_to='/a/' )
	Test_FilePathField			= models.FilePathField()
#	Test_FileField				= models.FileField( blank=True, null=True, upload_to='/a/' )#上传处理不成功~
	
	Test_IntegerField		= models.IntegerField()
	Test_FloatField			= models.FloatField()
	Test_CommaSeparatedIntegerField		= models.CommaSeparatedIntegerField( max_length=50 )
	Test_BooleanField			= models.BooleanField()
#	Test_AutoField				= models.AutoField()#自增长字段。
	Test_DecimalField			= models.DecimalField( max_digits=5, decimal_places=2 )#有精确位数的十进制小数，等同于 Python 中的 Decimal 实例。有两个必需的参数：DecimalField.max_digits~数字的整体位数。DecimalField.decimal_places~整体位数中包含的小数位数。比如：345.67 
	
	
	#方法1.婴儿潮状态（字符串）
	def baby_boomer_status(self):
		"Returns the person's baby‐boomer status."
		import datetime
		if datetime.date(1945, 8, 1) <= self.birth_date <= datetime.date(1964, 12, 31):
			return "Baby boomer"
		if self.birth_date < datetime.date(1945, 8, 1):
			return "Pre‐boomer"
		return "Post‐boomer"
	
	#方法2.是否中西部（True或False）
	def is_midwestern(self):
		"Returns True if this person is from the Midwest."
		return self.state in ('IL', 'WI', 'MI', 'IN', 'OH', 'IA', 'MO')
	
	#方法3.	全名（Unicode字符串）
	def _get_full_name(self):
		"Returns the person's full name."
		return u'%s %s' % (self.first_name, self.last_name)
		
	full_name 			= property( _get_full_name )			#property是说强制访问私有属性 _get_full_name 吗~？






class Publisher(models.Model):
	name 				= models.CharField( max_length=30, verbose_name='出版社名称' )
	address 			= models.CharField( max_length=50, verbose_name='地址' )
	city 				= models.CharField( max_length=60, verbose_name='城市' )
	state_province 		= models.CharField( max_length=30, verbose_name='省份' )
	country 			= models.CharField( max_length=50, verbose_name='国家' )
	website 			= models.URLField( blank=True, null=True, verbose_name='官方网站' )
	
	def __unicode__(self):
		return self.name
		
	#指定缺省的排序META~~~
	class Meta:
		ordering = ['-name']
		
		
class Author(models.Model):
	first_name 		= models.CharField( max_length=30, verbose_name='名' )
	last_name 		= models.CharField( max_length=40, verbose_name='姓氏' )	#i18n
	email 			= models.EmailField( blank=True, verbose_name='e-mail' )
#	name = models.CharField(help_text=_('This is the help text'))
	
	def __unicode__(self):
		return u'%s %s' % ( self.first_name, self.last_name )
		
		



class BookManager(models.Manager):
	'Manager方法，为模块添加表级功能（方法）的首选办法。'
	def title_count( self, keyword ):
		return self.filter( title__icontains = keyword ).count()


class Book(models.Model):
	title 				= models.CharField( max_length=100, verbose_name='书名' )
	authors 			= models.ManyToManyField( Author, verbose_name='author\'s' )	#多对多的字段；会自生成称一个中间表，中间表里衔接着当前Book表的id 和 另一张表Author（当前定义的）的id~同时当前Book表中啥字段也没有生成，只会在链接关系时在中间表生成对应关系~
	publisher 			= models.ForeignKey( Publisher, verbose_name='出版商' )	#外键的字段；只会自动生成一个Publisher_id字段~
	
	publication_date 	= models.DateField( blank=True, null=True, unique_for_date='publication_date', verbose_name='出版日期' )
	#在 DateField 或 DateTimeField 字段设置该unique_for_date选项，那么字段的值就必须是不可重复的。
	#比如，如果你又一个名为 title 的字段包含这个选项 —— unique_for_date="pub_date" —— ，那么 Django 就不会允许两个记录有相同的 title 和 pub_date。这在 Django 管理表单级别有效，而不在数据库级别执行！！！。（此处只用于测试，不符合生活中的逻辑，这将会导致出版的书日期不能和另一本的日期相同！记住，这只是表单级别的验证！！！）
	
	num_pages			= models.IntegerField( verbose_name='页码' )		#更新修改表结构~然后，请运行命令 python manage.py sqlall books 来查看CREATE TABLE语句。
	
	objects				= BookManager()		#牛气，新增的伪字段（DB中并没添加此字段）。我估摸着是窗口函数！且可以添加多个方法
	
	
#	photo 				= models.FileField( upload_to='d:/test/djangoweb/mysite/photos', blank=True )
	
	
	
	
	def __unicode__(self):
		return self.title



class BookPhoto(models.Model):
	book 	= models.ForeignKey(Book)
	image 	= models.ImageField( upload_to='bookphotos', blank=True ) 













import uuid

class Chapter(models.Model):
    id    		= models.AutoField(primary_key=True)
    book  		= models.ForeignKey(Book)
    title 		= models.CharField(max_length=100)
    seotitle  	= models.CharField(max_length=128)
    weight    	= models.IntegerField(default=0)
    description = models.TextField()
    tags     	= models.CharField(max_length=128,blank=True)

class Lession(models.Model):
    id       		= models.AutoField(primary_key=True)
    chapter  		= models.ForeignKey(Chapter)
    title    		= models.CharField(max_length=128)
    subtitle 		= models.CharField(max_length=128, blank=True)
    seotitle 		= models.CharField(max_length=128, blank=True)
    summary  		= models.TextField(blank=True)
    content  		= models.TextField()
    tags     		= models.CharField(max_length=128,blank=True)
    
    time_created  	= models.DateTimeField( auto_now_add=True )
    time_modefied 	= models.DateTimeField( auto_now=True )
    time_replied  	= models.DateTimeField( auto_now_add=True )
    
    counter_staied  = models.IntegerField( default=0, editable=False )
    counter_visited = models.IntegerField( default=0 )
    counter_replied = models.IntegerField( default=0 )
    
    weight 			= models.IntegerField( default=0 )
    uuid   			= models.CharField( max_length=40, unique=True, db_index=True, default=uuid.uuid1 )
    enable 			= models.BooleanField( default=True )
    has_attachment 	= models.FileField( upload_to='book_attachment', blank=True )















    
    
















