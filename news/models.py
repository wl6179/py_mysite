# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Reporter(models.Model):
    full_name = models.CharField(max_length=70)

    def __unicode__(self):
        return self.full_name




from mysite.classes.models import CXBG_product_class

class Article(models.Model):
    pub_date = models.DateTimeField()
    headline = models.CharField(max_length=200)
    content = models.TextField()
    reporter = models.ForeignKey(Reporter)
    cxbg_product_class = models.ForeignKey(CXBG_product_class)#----------------------
    

    def __unicode__(self):
        return self.headline


from django import forms
from django.contrib import admin
class Class_A(models.Model):
    classname	= models.CharField(max_length=30)
    parent		= models.ForeignKey( 'self', related_name="munchie", null=True, blank=True )
    def __unicode__(self):
        return self.classname
    class Meta:  
        verbose_name = "嗯分类"  			#有点像我的unit单位名称变量！~
        verbose_name_plural = "无敌分类s"	#整个模型的显示名~
class Class_AForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Class_AForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:		#'instance'为何挨这么近？！~
            self.fields['parent'].queryset = Class_A.objects.exclude( id=kwargs['instance'].id )
class Class_AAdmin(admin.ModelAdmin):
    model = Class_A
    form  = Class_AForm
    list_display 	= ( 'classname', 'parent' )		#列表显示字段~	（针对列表时）
    list_select_related = True
    list_filter 		= ( 'parent__classname', )		#筛选功能之 父级分类的筛选~	（针对列表时）
    ordering 		= ['-classname']
admin.site.register( Class_A, Class_AAdmin )



class Class_B(models.Model):
    classname	= models.CharField(max_length=30)
    parent		= models.ForeignKey( 'self', related_name="munchie", verbose_name='parent menu', null=True, blank=True )
    ddddd		= models.ForeignKey( Class_A, null=True, blank=True )

    def __unicode__(self):
        return self.classname


class Class_C(models.Model):
    classname	= models.CharField(max_length=30)
    parent		= models.ForeignKey( 'self', related_name="munchie", null=True, blank=True )

    def __unicode__(self):
        return self.classname
















from django.utils.safestring import *
#分类设计。（和其他模块一起放在这里不好！应该单独app，否则其它app无法引用~）
class CXBG_product_class(models.Model):
    classname    	= models.CharField( max_length=30, verbose_name='abc名' )
    readme 			= models.TextField( verbose_name='说明' )
    orderid  		= models.IntegerField( default=100, help_text="注意: <em style='color:red'>越大越靠前，默认为100</em>.", verbose_name='排序' )
    parent  		= models.ForeignKey( 'self', related_name="abc", null=True, blank=True, help_text="注意: <em style='color:red'>没有父类代表是顶级类</em>.", verbose_name='父类' )#关联自己
    parentpath 		= models.CommaSeparatedIntegerField( max_length=18, default='0', verbose_name='父类路径图' )
    depth  			= models.IntegerField( default=0, verbose_name='深度' )
    rootid  		= models.IntegerField( verbose_name='根级别划分集群id' )
    child     		= models.IntegerField( default=0, verbose_name='子类数' )#models.FloatField()适合金额e字段！#models.CommaSeparatedIntegerField( max_length=50 )由逗号,分隔开的数字组e字段！
    photo     		= models.ImageField( upload_to='cphotos', blank=True, verbose_name='图片' )#models.FilePathField()
    enable 			= models.BooleanField( default=True, verbose_name='是否显示' )#models.NullBooleanField()
    adddate  	= models.DateTimeField(auto_now_add=True)
    modifydate 	= models.DateTimeField(auto_now=True)
    #方
    #def colored_name(self):
    #    return '<span style="color: #%s;">%s %s</span>' % (self.color_code, self.first_name, self.last_name)
    #colored_name.allow_tags 	= True
    #full_name 					= property( _get_full_name )#************************
    #	return self.state in ('IL', 'WI', 'MI', 'IN', 'OH', 'IA', 'MO')
    #------------------------------------------------------------------------------------------------------------------------
    #方法1.（用来显示）分析当前分类的地位，并构造其如何显示其层次，此方法函数等于新增一聚合字段。（好处是可以进行深入处理！~）
    def classname_supper(self):
        "Returns 分类显示字符（包括等级层次表示字符如--）."
        #return self.classname + '啊啊啊'#（报错！）如有中文要加u原字符！！
        #return u'%s %s' % ( self.classname, u'啊啊啊' )#（正确！）
        #return mark_safe(”<a href=’/accounts/%s/’>%s</a>” %(self.user.id, self.user.username)) —— 使用mark_safe函数标记后，django将不再对该函数的内容进行转义！~(但一定要导入from django.utils.safestring import mark_safe )
        if self.depth>0:
        	return mark_safe( "%s %s" %(self.depth * " -- ", self.classname) )#<img src=/static/images/tree_line.gif />不行还是被转义！~
        return self.classname
    #------------------------------------------------------------------------------------------------------------------------
    #aaa = property( classname_supper(self) )
    def __unicode__(self):
        return "%s %s" %(self.depth * " -- ", self.classname)
    class Meta:  
        verbose_name = "标准分类"  			#有点像我的unit单位名称变量！~
        verbose_name_plural = "标准分类s"	#整个模型的显示名~
        ordering 			= [ 'rootid', 'orderid' ]#作用于（外链显示时）的下拉菜单列表！
class CXBG_product_classForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CXBG_product_classForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:		#'instance'为何挨这么近？！~
            self.fields['parent'].queryset = CXBG_product_class.objects.exclude( id=kwargs['instance'].id )
class CXBG_product_classAdmin(admin.ModelAdmin):
    model = CXBG_product_class
    form  = CXBG_product_classForm
    list_display 		= ( 'classname_supper', 'readme','parent', 'orderid', 'parentpath', 'depth', 'rootid', 'child', 'photo', 'enable', 'adddate' )		#列表显示字段~	（针对列表时）???? 如何定制 ?????
    list_select_related = True
    list_filter 		= ( 'parent__classname', )		#筛选功能之 父级分类的筛选~	（针对列表时）
    ordering 			= [ 'rootid', 'orderid' ]#作用于后台admin列表！
admin.site.register( CXBG_product_class, CXBG_product_classAdmin )














#自定义admin表单的显示！!!!!!!!!!!!!!!!!!!!!!!!!wangliang!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!---------====================：
from django import forms
from django.contrib import admin

class Menu(models.Model):
    title = models.CharField('title', max_length=50, unique=True)
    parentMenu = models.ForeignKey('self', verbose_name='parent menu',blank=True, null=True)
    def __unicode__(self):
        return self.title

#admin的表单会有变化~
class MenuForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        if'instance'in kwargs:		#'instance'为何挨这么近？！~
            self.fields['parentMenu'].queryset = Menu.objects.exclude(id=kwargs['instance'].id)		#排除掉自己的id，在parentMenu外键下拉中~（个性化某一个字段!）
            
class MenuAdmin(admin.ModelAdmin):
    model = Menu
    form  = MenuForm


admin.site.register( Menu, MenuAdmin )

#自定义admin表单的显示！!!!!!!!!!!!!!!!!!!!!!!!!wangliang!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!---------====================：