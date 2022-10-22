#encoding: utf-8
from utils import restful
from django.shortcuts import redirect

def my_login_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:   # 当前用户已经登录了
            return func(request,*args,**kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message='请先登录！')
            else:
                return redirect('/')

    return wrapper