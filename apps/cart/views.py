from django.shortcuts import render
from .models import Order,Orderitem
from utils import restful
from django.conf import settings
from django.shortcuts import reverse

def cart_index(request):
    buyer = request.user
    if not request.user.is_authenticated:
        return restful.params_error(message="请先登录！")
    if Order.objects.filter(status=1).count() == 0:
        orderitem = None
        order = None
    else:
        order = Order.objects.get(buyer=buyer, status=1)
        orderitem = Orderitem.objects.filter(order_id=order)
    context = {
        'order': order,
        'orderitem': orderitem,
    }
    return render(request, 'course/course_index.html', context=context)

from apps.goods.models import Goods
from django.db.models import F
def add_cart(request):
    goods_id = int(request.GET.get('goods_id'))
    goods = Goods.objects.get(pk=goods_id)  # goods_id对应的实体模型
    goods_price = float(request.GET.get('goods_price'))
    buyer = request.user    # 当前登录的用户
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        return restful.params_error(message="请先登录！")

    try:        # get返回值只能由一条记录，多条或者空都会报错
        buyer_order = Order.objects.get(buyer=buyer, status=1)
    except:     # 同一个用户同时只允许有一条未完成的订单，报错说明没有未完成的订单，那就新建一个订单
        buyer_order = Order.objects.create(buyer=buyer,amount=0)
    # 获取订单详情，根据goods_id和当前用户查询是否存在这条商品的数据
    orderitem = Orderitem.objects.filter(goods_id=goods,order_id=buyer_order)
    if orderitem:   # 如果存在，将数量+1
        # print(orderitem.values()[0].get("num"))
        orderitem.update(num=F("num")+1)
        print("if")
    else:       # 如果不存在，新建一条详情数据
        Orderitem.objects.create(order_id=buyer_order, goods_id=goods, price=goods_price, num=1)
        print("else")

    item = Orderitem.objects.get(order_id=buyer_order, goods_id=goods)  # 找到新添加的这条数据
    Order.objects.filter(buyer=buyer, status=1).update(amount=F("amount") + goods_price)     # 重复添加，order中价格该怎么计算

    return restful.ok()



def delete_cart(request):
    order_id = str(request.POST.get('order_id'))
    item_id = int(request.POST.get('item_id'))

    orderitem = Orderitem.objects.get(pk=item_id)
    print(orderitem.price)
    print(order_id)
    order = Order.objects.filter(uid=order_id)
    print(order)

    if orderitem.num > 1:
        Orderitem.objects.filter(pk=item_id).update(num=F("num") - 1)
        Order.objects.filter(pk=order_id).update(amount=F("amount") - orderitem.price)
    elif orderitem.num == 1:
        Order.objects.filter(pk=order_id).update(amount=F("amount") - orderitem.price)
        Orderitem.objects.filter(pk=item_id).delete()



    return restful.ok()


from .utils import alipay_obj
def check_out(request):
    if request.method == 'GET':
        return render(request, 'a.html')
    # 如果是post，我们认为是购买
    # 示例化一个对象
    alipay = alipay_obj()

    order_id = request.POST.get("order")
    # out_trade_no = Order.objects.get(pk=order_id).pk
    out_trade_no = Order.objects.get(pk=order_id).order_code
    total_amount = Order.objects.get(pk=order_id).amount
    orderitem = Orderitem.objects.filter(order_id=order_id)
    swap = []
    for obj in orderitem:
        swap.append(obj.goods_id.name)
    subject = '，'.join(swap)

    # print(order_id)
    print(out_trade_no)
    # print(total_amount)
    # print(subject)

    # 生成支付路由
    # 拼接url--返回url
    # 电脑网站支付，需要跳转到：https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        # 这下面的数据，都应该是你数据库的数据，但是我这里做测试，直接写死了
        # out_trade_no=out_trade_no,  # 商品订单号  唯一的
        out_trade_no=out_trade_no,  # 商品订单号  唯一的
        total_amount=total_amount,  # 商品价格
        subject=subject,  # 商品的名称
        return_url=settings.ALIPAY_SETTING.get('ALIPAY_RETURN_URL'),  # 同步回调网址--用于前端，付成功之后回调
        notify_url=settings.ALIPAY_SETTING.get('ALIPAY_NOTIFY_URL')  # 异步回调网址---后端使用，post请求，网站未上线，post无法接收到响应内容
    )
    # 我这里大概讲一下为什么要有同步/异步，因为同步是前端的，
    # 如果前端出现页面崩了，那么校验有后端完成，
    # 而且在实际开发中，后端一定要校验，因为前端的校验，可被修改
    url = 'https://openapi.alipaydev.com/gateway.do' + '?' + order_string
    # return JsonResponse({'url': url, 'status': 1})
    return restful.result(data={'url': url, 'status': 1})

from django.http import JsonResponse, HttpResponse
# def check_html_view(request):
#     if request.method == "GET":
#         # 进行校验，因为支付成功之后，后端是不知道是否成功的，所以需要校验一下
#         alipay = alipay_obj()
#         data = request.GET.dict()  # 把get请求的参数转换成字典
#         signature = data.pop("sign")  # 把sign pop出去
#         # verification
#         success = alipay.verify(data, signature)  # success ----> True False
#         # 上面的都是固定用法
#         if success:
#             # 如果成功支付了，这个success是True
#             # 接着写逻辑了，比如修改当前订单的状态
#             # 我举一个例子
#             print('支付成功，后台已经校验过了，金币+1')
#             return HttpResponse('ok')
#
#         return HttpResponse('支付失败')

from django.http import HttpResponseRedirect
def check_html_view(request):
    if request.method == "GET":
        # 进行校验，因为支付成功之后，后端是不知道是否成功的，所以需要校验一下
        alipay = alipay_obj()
        data = request.GET.dict()  # 把get请求的参数转换成字典
        signature = data.pop("sign")  # 把sign pop出去
        # verification
        success = alipay.verify(data, signature)  # success ----> True False
        if success:
            # 如果成功支付了，这个success是True
            # 接着写逻辑了，比如修改当前订单的状态
            Order.objects.filter(status=1).update(status=2)
            print('支付成功，后台已经校验过了')
            return HttpResponseRedirect('/')

        return restful.params_error(message="支付失败")
    # post 请求异步回调校验，最后一定要返回一个success
    alipay = alipay_obj()
    data = request.GET.dict()
    signature = data.pop("sign")
    # verification
    success = alipay.verify(data, signature)  # True False
    if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
        print('支付成功，后台已经校验过了')
        return restful.ok()
    return restful.params_error(message="支付失败")