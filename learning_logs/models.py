from django.db import models
from django.contrib.auth.models import User

# Create your models here.

'''
为了禁止用户访问其他用户的数据，需要将用户与数据关联。只需要将最高层的数据关联到用户，这样更低层的
数据将自动关联到用户:
'''

class Topic(models.Model):
    '''用户学习的主题'''
    text = models.CharField(max_length=200) #限制字段的长度
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        '''返回模型的字符串表示'''
        return self.text
    
    
    
class Entry(models.Model):
    '''学到的有关某个主题的具体知识'''
    
    #由于和topic是多对一的关系，所以这里entry和topic是的外键
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  #这里在2.0版本后需添加on_delete参数
    text = models.TextField()   #不限制字段的长度
    date_added = models.DateField(auto_now_add=True)   #记录日期和时间的数据
    '''这里改为DateTimeField会出错，还未找出原因'''
    class Meta:   #用于存储 用于管理模型的额外信息
        verbose_name_plural = 'entries' #这里为保证entry多于一个时，使用entries而非entrys(默认)显示
        
    def __str__(self):
        '''返回模型的字符串表示'''
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text