from django.db import models

class GoodsCategory(models.Model):
    name = models.CharField(max_length=100)

class Goods(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    thumbnail = models.URLField()
    content = models.TextField()
    category = models.ForeignKey('GoodsCategory',on_delete=models.SET_NULL,null=True)

class Comment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    goods = models.ForeignKey("Goods",on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey("my_auth.User",on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_time']

# 轮播图
class Banner(models.Model):
    priority = models.IntegerField(default=0)   #优先级
    image_url = models.URLField()
    link_to = models.URLField()
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority']