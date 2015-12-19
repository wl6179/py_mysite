# -*- coding: utf-8 -*-
from django.db import models

from django import forms
from django.contrib import admin


#处理Ueditor以及其他的公共函数.
from mysite import functions
from django.db.models import Max


# Create your models here.
from django.utils.safestring import *
#分类设计。
class CXBG_product_class(models.Model):
    classname    	= models.CharField( max_length=30, verbose_name='abc名' )
    readme 			= models.TextField( blank=True, verbose_name='说明' )
    orderid  		= models.IntegerField( default=100, help_text="注意: <em style='color:red'>越大越靠前，默认为100</em>.", verbose_name='排序' )
    parent  		= models.ForeignKey( 'self', related_name="abc", null=True, blank=True, help_text="注意: <em style='color:red'>没有父类代表是顶级类</em>.", verbose_name='父类' )#关联自己
    parentpath 		= models.CommaSeparatedIntegerField( max_length=18, default='0', verbose_name='父类路径图' )
    depth  			= models.IntegerField( default=0, verbose_name='深度' )
    rootid  		= models.IntegerField( verbose_name='根级别划分集群id', help_text="注意: <em style='color:red'>每一个一级类及其下子类为一个‘集群’</em>." )
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
    classname_supper.short_description = 'ABC名'#(Yeah！)（模仿abc名字段的显示字符，哈）
    #------------------------------------------------------------------------------------------------------------------------
    def is_root_now(self):
    	"Returns 分类是否属于根类."
        if self.depth == 0:
            return '根'
        return '子类'
    is_root_now.short_description = '是否根类?'#(Yeah！)
    
    #aaa = property( classname_supper(self) )
    def __unicode__(self):
        return "%s %s" %(self.depth * " -- ", self.classname)
    class Meta:  
        verbose_name 		= "标准分类"  			#有点像我的unit单位名称变量！~
        #verbose_name_plural = "标准分类s"	#整个模型的显示名~
        ordering 			= [ 'rootid', 'orderid' ]#作用于（外链显示时）的下拉菜单列表！
        verbose_name_plural = 'abc分类列表'#显示在导航条例，顶部。
    class Admin:
    	pass
    	#list_filter = ( 'rootid', )#？？？？？？
class CXBG_product_classForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CXBG_product_classForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:		#'instance'为何挨这么近？！~
            self.fields['parent'].queryset = CXBG_product_class.objects.exclude( id=kwargs['instance'].id )
class CXBG_product_classAdmin(admin.ModelAdmin):
    model = CXBG_product_class
    form  = CXBG_product_classForm
    list_display 		= ( 'classname_supper', 'is_root_now', 'parent', 'orderid', 'parentpath', 'rootid', 'depth', 'child', 'photo', 'enable', 'adddate' )#列表显示字段~（针对列表时）——定制了'classname_supper'！
    list_select_related = True
    ###book_fk_filter_by = 'rootid'
    #list_filter 		= ( 'parent__classname', )		#筛选功能之 父级分类的筛选~	（针对列表时）——（未完善！可注释掉~）
    ordering 			= [ 'rootid', 'orderid' ]#作用于后台admin列表！
    exclude 			= [ 'photo', 'parentpath', 'depth', 'rootid' ]#不显示某些字段！
    list_editable 		= ['parent', 'orderid', 'parentpath', 'rootid', 'depth', 'child']#能编辑的某些字段！（就在列表中！！！！！！！！！！！！！！！！！！！！！！！！！！！！！）
    search_fields 		= ['classname', 'parent__classname']#搜索字段！
    #formfield_overrides = {
    #    models.TextField: {'widget': RichTextEditorWidget},
    #}#启用django内置的富文本框！（但是需要自定义控件myapp.widgets，即from myapp.widgets import RichTextEditorWidget）
    def save_model(self, request, obj, form, change):
        "重写数据处理细节，原装super(BlogABC, self).save()"
        if not change:	#如果是新增记录的话（就）
            if not request.POST['parent']:		#根分类
                try:
                	last_class_rootid = CXBG_product_class.objects.order_by('-rootid', '-orderid' )[0]	#获取分类中rootid最大的值.
                except:
                	last_class_rootid = False
                #last_class_orderid = CXBG_product_class.objects.order_by('-rootid', '-orderid' )[0]	#获取同一档分类中orderid最大的值.
                obj.parentpath 	= '0'
                obj.depth 		= 0
                if last_class_rootid:	#如果有了分类记录，则计算最大rootid当前.
                    obj.rootid 	= 1 + last_class_rootid.rootid 	#用rootid最大的值 + 1 来新增新根类 之rootid！
                else:					#如果没有任何记录，则第一个根分类的rootid为1.
                    obj.rootid 	= 1								#或1.
                obj.child 		= 0
                obj.orderid 	= 0		#orderid从0(根)开始递增.（在同一档rootid的分类大集合中！）
    	        obj.save()				#重要！不写则不会保存任何记录！
    	        
            else:								#子分类（此时request.POST['parent']有传值，父类的id！）
                parent_object = CXBG_product_class.objects.filter( id = request.POST['parent'] )[0]				#获取父级分类对象.一定要用[0]
                obj.parentpath 	= '%s,%d' % ( parent_object.parentpath ,parent_object.id )	#继承父类的path；同时加上父类的id上去！别忘了逗号.
                obj.depth 		= parent_object.depth + 1									#继承父类的depth，并且+1.
                obj.rootid		= parent_object.rootid										#完全继承父类的rootid.
                obj.child 		= 0															#等于0.
                CXBG_product_class.objects.filter( id = request.POST['parent'] ).update( child = parent_object.child + 1 )#更新：所在父类child加1！
                #orderid继承父类的orderid并且加1；（当前父类下的子类中最大的orderid+1，没有就用父类的orderid+1 ！！！）
                try:
                    subclasses_object = CXBG_product_class.objects.filter( parent__id = request.POST['parent'] )
                    SubClasses_MaxOrderID = subclasses_object.aggregate(Max('orderid'))['orderid__max']
                    obj.orderid = SubClasses_MaxOrderID + 1			#(此父类下有子类时~)
                except:
                    obj.orderid = parent_object.orderid + 1		#（此父类要是没有子类时~）
                
                #orderid对排在当前分类后边的同档分类的orderid全部都加1；
                ###CXBG_product_class.objects.filter( parentpath__startswith = '%s,%d' % ( rootid = parent_object.rootid,  orderid__gt = parent_object.orderid ).update( orderid =+ 1 )
                ###CXBG_product_class.objects.extra( select={'class_excute_now': 'UPDATE classes_cxbg_product_class SET orderid=orderid+1 WHERE rootid=%d AND orderid>%d' % ( parent_object.rootid, parent_object.orderid )} )
                my_custom_sql( 'UPDATE classes_cxbg_product_class SET orderid=orderid+1 WHERE rootid=%d AND orderid>%d' % ( parent_object.rootid, (obj.orderid-1) ) )#更新所有排序.
                #CXBG_product_class.objects.filter( parentpath__startswith = '%s,%d' % ( parent_object.parentpath ,parent_object.id ), rootid = parent_object.orderid + 1, orderid__gt = parent_object.orderid ).update( orderid = orderid + 1 )
                obj.save()
                
        else:			#如果是修改的话（就）
            #if request.POST['parent'] == obj.parent:		#如果父类没变化，不做特殊处理.
            #super(CXBG_product_class, self).save()
            obj.save()
            #pass
#        if getattr(obj, 'added_by', None) is None:#如果added_by字段传值为空...
#            obj.added_by = request.user#自动获取值...
#        obj.last_modified_by = request.user
#        obj.save()
admin.site.register( CXBG_product_class, CXBG_product_classAdmin )
#        else:			#如果是修改的话（就）
#            if request.POST['parent'] == obj.parent:		#如果父类没变化，不做特殊处理.
#    	        obj.save()				#重要！不写则不会保存任何记录！
#    	        
#            else:												#如果父类选择有了变化，特殊处理.
#                if not request.POST['parent']:		#根分类
#                    last_class_rootid = CXBG_product_class.objects.order_by('-rootid', '-orderid' )[0]	#获取分类中rootid最大的值.
#                    obj.parentpath 	= '0'
#                    obj.depth 		= 0
#                    if last_class_rootid:	#如果有了分类记录，则计算最大rootid当前.
#                        obj.rootid 	= 1 + last_class_rootid.rootid 	#用rootid最大的值 + 1 来新增新根类 之rootid！
#                    else:					#如果没有任何记录，则第一个根分类的rootid为1.
#                        obj.rootid 	= 1								#或1.
#                    obj.child 		= 0
#                    #--------------（牵扯）
#                    if obj.parent:#如果原本属于某一个父级分类，令此父级分类的child减1.
#                    	parent_object_original = CXBG_product_class.objects.filter( id = obj.parent.id )[0]				#获取父级分类对象.一定要用[0]
#                    	CXBG_product_class.objects.filter( id = obj.parent.id ).update( child = parent_object_original.child - 1 )#所在原本父类child减1！
#                    #--------------（牵扯）
#                else:								#子分类（此时request.POST['parent']有传值，父类的id！）
#                    parent_object = CXBG_product_class.objects.filter( id = request.POST['parent'] )[0]				#获取父级分类对象.一定要用[0]
#                    obj.parentpath 	= '%s,%d' % ( parent_object.parentpath ,parent_object.id )	#继承父类的path；同时加上父类的id上去！别忘了逗号.
#                    obj.depth 		= parent_object.depth + 1									#继承父类的depth，并且+1.
#                    obj.rootid		= parent_object.rootid										#完全继承父类的roodid.
#                    obj.child 		= 0															#等于0.
#                    CXBG_product_class.objects.filter( id = request.POST['parent'] ).update( child = parent_object.child + 1 )#所在父类child加1！
#                    #--------------（牵扯）
#                    if obj.parent.id:#如果原本属于某一个父级分类，令此父级分类的child减1.
#                	    parent_object_original = CXBG_product_class.objects.filter( id = obj.parent.id )[0]				#获取父级分类对象.一定要用[0]
#                	    CXBG_product_class.objects.filter( id = obj.parent.id ).update( child = parent_object_original.child - 1 )#所在原本父类child减1！
#                    #--------------（牵扯）
#                    obj.save()
def my_custom_sql(sql_myself):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute( sql_myself )
    connection.commit()