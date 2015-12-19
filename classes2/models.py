# -*- coding: utf-8 -*-
from django.db import models

from django import forms
from django.contrib import admin


from django.db.models import Max


# Create your models here.
from django.utils.safestring import *
#分类设计。
class CXBG_product_class(models.Model):
    classname    	= models.CharField( max_length=30, verbose_name='abc名' )
    readme 			= models.TextField( verbose_name='说明' )
    orderid  		= models.IntegerField( default=100, help_text="注意: <em style='color:red'>越大越靠前，默认为100</em>.", verbose_name='排序' )
    parent  		= models.ForeignKey( 'self', related_name="abc", null=True, blank=True, help_text="注意: <em style='color:red'>没有父类代表是顶级类</em>.", verbose_name='父类' )#关联自己
    parentpath 		= models.CommaSeparatedIntegerField( max_length=18, default='0', verbose_name='父类路径图' )
    depth  			= models.IntegerField( default=0, verbose_name='深度' )
    rootid  		= models.IntegerField( verbose_name='根级别划分集群id', help_text="注意: <em style='color:red'>每一个一级类及其下子类为一个‘集群’</em>." )
    child     		= models.IntegerField( default=0, verbose_name='子类数' )#models.FloatField()适合金额e字段！#models.CommaSeparatedIntegerField( max_length=50 )由逗号,分隔开的数字组e字段！
    previd			= models.IntegerField( default=0, verbose_name='上一个分类id' )
    nextid			= models.IntegerField( default=0, verbose_name='下一个分类id' )
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
        verbose_name_plural = "标准分类s"	#整个模型的显示名~
        ordering 			= [ 'rootid', 'orderid', 'id' ]#作用于（外链显示时）的下拉菜单列表！
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
    list_display 		= ( 'classname_supper', 'is_root_now', 'parent', 'orderid', 'parentpath', 'depth', 'rootid', 'child', 'photo', 'enable', 'adddate' )#列表显示字段~（针对列表时）——定制了'classname_supper'！
    list_select_related = True
    ###book_fk_filter_by = 'rootid'
    list_filter 		= ( 'parent__classname', )		#筛选功能之 父级分类的筛选~	（针对列表时）——（未完善！可注释掉~）
    ordering 			= [ 'rootid', 'orderid', 'id' ]#作用于后台admin列表！
    exclude 			= [ 'photo', 'parentpath', 'depth', 'rootid', 'previd', 'nextid' ]#不显示某些字段！
    list_editable 		= [ 'parent', 'orderid', 'parentpath', 'depth', 'rootid', 'child' ]#能编辑的某些字段！（就在列表中！！！！！！！！！！！！！！！！！！！！！！！！！！！！！）
    search_fields 		= [ 'classname', 'parent__classname' ]#搜索字段！
    #formfield_overrides = {
    #    models.TextField: {'widget': RichTextEditorWidget},
    #}#启用django内置的富文本框！（但是需要自定义控件myapp.widgets，即from myapp.widgets import RichTextEditorWidget）
    def save_model(self, request, obj, form, change):
        "重写数据处理细节"
        if not change:	#如果是新增记录的话（就）
            #last_class_rootid = CXBG_product_class.objects.order_by('-rootid', '-orderid', '-id')[0]	#获取分类中rootid最大的值.
            rs = CXBG_product_class.objects.all()
#            a=CXBG_product_class.objects.extra(
#	            select={
#		            'class_max': 'SELECT MAX(*) FROM classes2_cxbg_product_class WHERE 1 = 1'
#		            }
#            )
            Maxid = rs.aggregate(Max('id')).get("id__count")
            #Maxid = a.class_max#...!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if not Maxid:
            	Maxid = 0
            theid = Maxid + 1
            MaxRootID = rs.aggregate(Max('rootid'))
            if not MaxRootID:
            	MaxRootID = 0
            RootID = MaxRootID + 1
            
            if request.POST['parent']>0:
            	rs1 = CXBG_product_class.objects.filter(id = request.POST['parent'])[0]
            	if rs1:
            		RootID 		= rs1.rootid
            		ParentName 	= rs1.classname
            		ParentDepth	= rs1.depth
            		ParentPath	= rs1.parentpath
            		Child		= rs1.child
            		ParentPath	= '%s,%d' % ( ParentPath ,rs1.id )
            		PrevOrderID	= rs1.rootid
            		if Child>0:
            			#得到与本分类同级的最后一个分类的OrderID
            			PrevOrderID = CXBG_product_class.objects.filter(id = request.POST['parent'])[0].aggregate(Max('orderid'))
            			trs = CXBG_product_class.objects.filter( parent = request.POST['parent'], orderid=PrevOrderID )[0]
            			PrevID = trs.id
            			
            			#得到同一父分类但比本分类级数大的子分类的最大OrderID，如果比前一个值大，则改用这个值。
            			PrevOrderID2 = CXBG_product_class.get_object( Q(parentpath__startswith = '%s,' % ( ParentPath )) )[0].aggregate(Max('orderid'))
            			if PrevOrderID2:
            				if PrevOrderID2 > PrevOrderID:
            					PrevOrderID = PrevOrderID2
            		else:
            			PrevID = 0
            			
            else:
            	if MaxRootID>0:
            		trs = CXBG_product_class.objects.filter( rootid = MaxRootID, depth=0 )[0]
            		PrevID = trs.id
            	else:
            		PrevID	= 0
            	PrevOrderID	= 0
            	ParentPath	= '0'
            #应该在此验证一下是否有重名分类！
            obj.rootid 		= RootID
            if request.POST['parent']>0:
            	obj.depth	= ParentDepth + 1
            else:
            	obj.depth	= 0
            obj.parentpath 	= ParentPath
            obj.orderid		= PrevOrderID
            obj.child		= 0
            obj.previd		= PrevID
            obj.nextid		= 0
    	    obj.save()				#重要！不写则不会保存任何记录！
            
        else:			#如果是修改的话（就）
            if request.POST['parent'] == obj.parent:		#如果父类没变化，不做特殊处理.
                pass
#
#	
#	'更新与本分类同一父分类的上一个分类的“NextID”字段值
#	if PrevID>0 then
#		conn.execute("update "& CurrentTableName &" set NextID=" & id & " where id=" & PrevID)
#	end if
#	
#	if ParentID>0 then
#		'更新其父类的子分类数
#		conn.execute("update "& CurrentTableName &" set child=child+1 where id="&ParentID)
#		
#		'更新该分类排序以及大于本需要和同在本分类下的分类排序序号
#		conn.execute("update "& CurrentTableName &" set OrderID=OrderID+1 where rootid=" & rootid & " and OrderID>" & PrevOrderID)
#		conn.execute("update "& CurrentTableName &" set OrderID=" & PrevOrderID & "+1 where id=" & id)
#	end if
            
            
admin.site.register( CXBG_product_class, CXBG_product_classAdmin )
