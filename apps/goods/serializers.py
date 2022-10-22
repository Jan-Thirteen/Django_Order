from rest_framework import serializers
from apps.goods.models import Goods,GoodsCategory,Comment,Banner
from apps.my_auth.serializers import UserSerializer

class GoodsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ('id','name')

class GoodsSerializer(serializers.ModelSerializer):
    category = GoodsCategorySerializer() # 表示category使用的是NewsCategorySerializer序列化
    # author = UserSerializer()
    class Meta:
        model = Goods
        fields = ('id','name','thumbnail','category','price')


class CommentSerizlizer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Comment
        fields = ('id','content','author','pub_time')

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id','image_url','priority','link_to')