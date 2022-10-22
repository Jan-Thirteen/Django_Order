# encoding: utf-8

from django.db import models
from shortuuidfield import ShortUUIDField

class Order(models.Model):
    uid = ShortUUIDField(primary_key=True)  # 主键
    order_code = models.IntegerField(unique=True) # 订单号  支付宝沙箱不支持字符串型的订单号
    buyer = models.ForeignKey("my_auth.User",on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)
    # 1：代表的是未支付。2：代表的是支付成功
    status = models.SmallIntegerField(default=1)

class Orderitem(models.Model):
    order_id = models.ForeignKey("Order",on_delete=models.CASCADE,related_name="order")
    goods_id = models.ForeignKey("goods.Goods",on_delete=models.DO_NOTHING)
    time = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(default=0)
    num = models.IntegerField(default=0)