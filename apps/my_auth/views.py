from django.shortcuts import render

from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm, RegisterForm
from utils import restful

# from django.views.decorators.csrf import ensure_csrf_cookie
# @ensure_csrf_cookie
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():  # 验证成功
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request, username=telephone, password=password)  # 进行验证，验证成功则返回user对象
        if user:
            if user.is_active:
                login(request, user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return restful.unauth(message="您的账号已经被冻结了！")
        else:
            return restful.params_error(message="手机号或者密码错误！")
    else:
        errors = form.get_errors()
        # {"password":['密码最大长度不能超过20为！','xxx'],"telephone":['xx','x']}
        return restful.params_error(message=errors)

from django.shortcuts import redirect,reverse
def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

from io import BytesIO
from django.http import HttpResponse
from utils.captcha.mycaptcha import Captcha
from django_redis import get_redis_connection   #redis
from django.core.cache import cache
def img_captcha(request):   # 图形验证码
    text,image = Captcha.gene_code()
    # BytesIO：相当于一个管道，用来存储图片的流数据
    out = BytesIO()
    # 调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out,'png')
    # 将BytesIO的文件指针移动到最开始的位置
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    # 从BytesIO的管道中，读取出图片数据，保存到response对象上
    response.write(out.read())
    response['Content-length'] = out.tell() #获取当前文件指针的位置

    # 12Df：12Df.lower()
    # cache.set(text.lower(),text.lower(),5*60)

    # redis_conn = get_redis_connection('default')
    # redis_conn.setex(key,second,value)
    #   key,value：键值对
    #   second：过期时间
    # redis_conn.setex(text.lower(),5*60,text.lower())

    cache.set(text.lower(), text.lower(), 5*60)

    return response

from utils.ronglianyun.example import SendMessage
from utils import restful
def sms_captcha(request):
    mobile = request.GET.get('telephone')
    code = Captcha.gene_text()  # 获取一个随机字符串
    datas = (code, '5')
    # mobile = '19810824612'
    # datas = ('12345', 5)

    # redis_conn = get_redis_connection('default')
    # redis_conn.setex(mobile,5*60,code)
    cache.set(mobile,code,5*60)
    print("短信验证码：",code)
    result = SendMessage.send_message(mobile, datas)    # todo 发送短信验证码
    print(result)
    return restful.ok()


""":cvar
    测试redis
"""
# from django.core.cache import cache
def cache_test(request):
    # todo  短信验证码测试
    cache.set('username', 'zhuyanyan', 10)
    result = cache.get('username')
    # redis_conn = get_redis_connection('default')
    # redis_conn.setex('username', 60, 'zhuyanyan')
    # result = redis_conn.get('username')
    # print(cache.get('username'))
    print(result)
    return HttpResponse('success')

from django.contrib.auth import get_user_model  # 从setting中获取模型
User = get_user_model()
@require_POST
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(telephone=telephone,username=username,password=password)
        login(request, user)    # 注册成功后直接登录
        return restful.ok()
    else:
        print(form.get_errors())
        return restful.params_error(message=form.get_errors())