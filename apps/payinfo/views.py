from django.shortcuts import render

def index(request):
    return render(request, 'payinfo/payinfo.html')



from .utils import alipay_obj
from django.conf import settings
from django.http import JsonResponse, HttpResponse


def good_list_view(request):
    if request.method == 'GET':
        return render(request, 'a.html')
    # 如果是post，我们认为是购买
    # 示例化一个对象
    alipay = alipay_obj()
    # 生成支付路由
    # 拼接url--返回url
    # 电脑网站支付，需要跳转到：https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        # 这下面的数据，都应该是你数据库的数据，但是我这里做测试，直接写死了
        out_trade_no="2016112528126",  # 商品订单号  唯一的
        total_amount=0.1,  # 商品价格
        subject='表,忙乎？砍一刀否',  # 商品的名称
        return_url=settings.ALIPAY_SETTING.get('ALIPAY_RETURN_URL'),  # 同步回调网址--用于前端，付成功之后回调
        notify_url=settings.ALIPAY_SETTING.get('ALIPAY_NOTIFY_URL')  # 异步回调网址---后端使用，post请求，网站未上线，post无法接收到响应内容
    )
    # 我这里大概讲一下为什么要有同步/异步，因为同步是前端的，
    # 如果前端出现页面崩了，那么校验有后端完成，
    # 而且在实际开发中，后端一定要校验，因为前端的校验，可被修改
    url = 'https://openapi.alipaydev.com/gateway.do' + '?' + order_string
    return JsonResponse({'url': url, 'status': 1})


def check_html_view(request):
    if request.method == "GET":
        # 进行校验，因为支付成功之后，后端是不知道是否成功的，所以需要校验一下
        alipay = alipay_obj()
        data = request.GET.dict()  # 把get请求的参数转换成字典
        signature = data.pop("sign")  # 把sign pop出去
        # verification
        success = alipay.verify(data, signature)  # success ----> True False
        # 上面的都是固定用法
        if success:
            # 如果成功支付了，这个success是True
            # 接着写逻辑了，比如修改当前订单的状态
            # 我举一个例子
            print('支付成功，后台已经校验过了，金币+1')
            return HttpResponse('ok')

        return HttpResponse('支付失败')