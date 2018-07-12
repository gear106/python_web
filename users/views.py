from django.shortcuts import render
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

def logout_view(request):
    '''注销用户'''
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))


def register(request):
    '''注册新用户'''
    if request.method != 'POST':
        # 显示空表单
        form = UserCreationForm()
    else:
        # 处理填写好的表单
        form = UserCreationForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            # 让用户自动登录， 再重新定向到主页
            # 注册时要求输入两次密码， 所以有password1和password2
            authenticated_user = authenticate(username=new_user.username, 
                                             password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))
        
    context = {'form':form}
    return render(request, 'users/register.html', context)  #这里把users写为user会报错找不到

            
            
            
            
            



            
            
            
            
            