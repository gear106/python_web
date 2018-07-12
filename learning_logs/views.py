from django.shortcuts import render, get_object_or_404
from .models import Topic, Entry
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    '''学习笔记主页'''
    #将请求的数据套用到模板中，然后返回给浏览器
    #第一个参数是原始的请求对象，第二个是可用于创建网页的模板
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    '''显示所有主题'''
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    '''显示单个主题及其所有的条目'''
    #通过Topic的id获得所有条目
    topic = get_objects_or_404(Topic, id=topic_id)
    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')  #-date_added前的减号表示降序排列
    # 将主题和条目都存储在字典中，再将其发送给模板topic.html:
    context = {'topic':topic, 'entries':entries}
    return render(request, 'learning_logs/topic.html', context)


'''
该函数需要处理两种情形：①刚进入new_topic网页，显示一个空表单；②对提交的表单数据进行处理，
并将用户重定向到网页topics:
    
创建Web应用程序时，将用到两种主要数据请求类型：GET请求和POST请求。从这俩英文单词可以看出，
如果只从服务器读取数据页面，则使用GET请求；如果要提交用户填写的表单，通常使用POST请求。
当然还有一些其他的请求类型，但这个项目中没有使用。本项目中处理表单都使用POST方法。

当不是POST请求时，我们生成一个空表单传递给模板new_topic.html，然后返回给用户；当请求是POST时，
我们从request.POST这个变量中获取用户提交的数据，并暂存到form变量中。

通过is_valid()方法验证表单数据是否满足要求：用户是否填写了所有必不可少的字段（表单字段默认都
是必填的），且输入的数据与字段类型是否一致。当然这些验证都是Django自动进行的。如果表单有效，
在通过form的save()方法存储到数据库，然后通过reverse()函数获取页面topics的URL，并将其传递给
HTTPResponseRedirect()以重定向到topics页面。如果表单无效，把这些数据重新传回给用户。
'''

@login_required
def new_topic(request):
    '''添加新主题'''
    if request.method != 'POST':    # request.method存储了请求的类型
        #未提交数据：创建一个空表单
        form = TopicForm()
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            # 添加新主题时关联到特定的用户
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            # 该类将用户重新定向到网页topics，函数reverse根据指定的URL模型确定URL
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form':form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    '''在特定的主题中添加新条目'''
    # topic_id 用于存储从URL中获得的值,这里没有回找不到具体的主题而报错
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # 让Django创建一个新的条目对象，并将其存储到new_entry,但不保存到数据库，
            # 待为这个新条目对象添加了属性topic之后再提交数据库。
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            # 将用户重新定向到显示相关主题的页面
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        # 初次请求，使用当前条目填充表单,若没有则只显示空的表单。
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)