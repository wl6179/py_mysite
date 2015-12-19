# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from django.db import models

class Poll(models.Model):
    question = models.CharField( '投票问题', max_length=200 )
    pub_date = models.DateTimeField('发布日期')
    
    def __unicode__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey( Poll, verbose_name = '所属投票问题（外键）')
    choice = models.CharField( '选项-描述文本', max_length = 200 )
    votes = models.IntegerField('投票数统计（此选择的）')
    image 	= models.ImageField(upload_to='pollphotos') 
    
    def __unicode__(self):
        #return self.poll.question
        return self.choice