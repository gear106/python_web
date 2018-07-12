'''定义users的URL模式'''

from django.urls import path
from django.contrib.auth.views import login
from . import views

'''
使用Django自带的login视图函数（注意，参数是login，而不是views.login）
从之前的例子可以看出，我们渲染模板的代码都是在自己写的视图函数中。但这
里使用了自带的视图函数，无法自行编写进行渲染的代码。所以，我们还传了一
个字典给path，告诉Django到哪里查找我们要用到的模板。注意，该模板在
users中，而不是在learning_logs中。
'''

app_name = 'users'
urlpatterns = [
        # 登录界面：
    path('login/', login, {'template_name': 'users/login.html'}, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    

]
