# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 23:01:15 2018

@author: GEAR
"""
'''
用户输入信息时，需要进行验证，确保提交的信息是正确的数据类型，且不是恶意信息，
如中断服务器的代码。然后再处理信息，并保存到数据库中。当然，这些工作很多都由
Django自动完成。
'''

from django import forms
from .models import Topic, Entry

'''
最简单的ModelForm版本只包含一个内嵌的Meta类，它告诉Django根据哪个模型创建表单，
以及在表单中包含哪些字段,我们根据Topic创建一个表单，该表单只包含字段text，并不
为该字段生成标签。
'''

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {"text": ""}

        #这里如果改为labels = {"text": " may"}，会在网页上显示标签may
        
        
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text':""}
        # 这里会在网页上显示一个文本框待用户输入：
        widgets = {'text':forms.Textarea(attrs={'cols':80})}
        
        
        