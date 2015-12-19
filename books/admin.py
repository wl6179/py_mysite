# -*- coding: utf-8 -*-
from django.contrib import admin
from mysite.books.models import Publisher, Author, Book, Person, BookPhoto, Chapter, Lession



class PersonAdmin( admin.ModelAdmin ):
	list_display = ( 'full_name', 'birth_date', 'state' )
	
	

class AuthorAdmin( admin.ModelAdmin ):
	list_display = ( 'first_name', 'last_name', 'email' )
	search_fields = ( 'first_name', 'last_name', 'email' )

class BookAdmin(admin.ModelAdmin):
	list_display = ( 'title', 'publisher', 'publication_date' )	#列表显示字段~	（针对列表时）
	list_filter = ( 'publication_date', )	#筛选功能之 出版日起筛选~			（针对列表时）
	date_hierarchy = 'publication_date'		#层次划分功能之 出版日层次划分导航~	（针对列表时）
	ordering = ( '-publication_date', )		#和models.py中的class Meta的ordering = ['-name']排序定义效果一致！~
#	fields = ( 'title', 'authors', 'publisher', 'publication_date' )	#陈列顺序，如果不配置，则按照module的来~

	filter_horizontal = ('authors',)		#不灵？？？！！！原因是：models.py中的模型使用了中文显示authors，所以authors功能异常！~是中文无法使用控件的问题！！~
	#还可以使用filter_vertical替代filter_horizontal！~功能一样，只是视觉效果不同。
	
	raw_id_fields = ( 'publisher', )	#不再是默认的下拉框，而是文本框了！（我个人还是喜欢下拉框！）


admin.site.register( Publisher )
admin.site.register( Author, AuthorAdmin )
admin.site.register( Book, BookAdmin )

admin.site.register( Person, PersonAdmin )


admin.site.register( BookPhoto )



admin.site.register( Chapter )
admin.site.register( Lession )