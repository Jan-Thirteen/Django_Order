from django.shortcuts import render
from .models import Goods,GoodsCategory,Banner
from django.conf import settings

def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT    # 每页展示的数量
    # select_related 同时查询外键
    goods = Goods.objects.select_related('category').all()[0:count]
    categories = GoodsCategory.objects.all()
    context = {
        'goods': goods,
        'categories': categories,
        'banners': Banner.objects.all()
    }
    return render(request, 'news/index.html', context=context)

from django.http import Http404
def goods_detail(request, goods_id):
    # select_related：提取外键字段
    # prefetch_related：反向引用
    try:
        goods = Goods.objects.select_related('category').prefetch_related('comments__author').get(pk=goods_id)
        context = {
            'goods': goods
        }
        return render(request, 'news/news_detail.html', context=context)
    except Goods.DoesNotExist:   # 当文章不存在才会抛出异常
        raise Http404

from utils import restful
from .serializers import GoodsSerializer
def goods_list(request):
    # 通过p参数，来指定要获取第几页的数据
    # 并且这个p参数，是通过查询字符串的方式传过来的/news/list/?p=2
    page = int(request.GET.get('p',1))
    # 分类为0：代表不进行任何分类，直接按照时间倒序排序
    category_id = int(request.GET.get('category_id',0))
    # 0,1
    # 2,3
    # 4,5
    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    if category_id == 0:    # 分类为0，不进行分类将所有数据一并返回
        # QuerySet
        # {'id':1,'title':'abc',category:{"id":1,'name':'热点'}}
        goods = Goods.objects.select_related('category').all()[start:end]
    else:   # 分类不为0，则按照分类查询
        goods = Goods.objects.select_related('category').filter(category__id=category_id)[start:end]
    serializer = GoodsSerializer(goods,many=True)
    data = serializer.data
    return restful.result(data=data)

from .forms import PublicCommentForm
from .models import Comment
from .serializers import CommentSerizlizer
from apps.my_auth.decorators import my_login_required   # 自定义装饰器
@my_login_required
def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        goods_id = form.cleaned_data.get('goods_id')
        content = form.cleaned_data.get('content')
        goods = Goods.objects.get(pk=goods_id)
        comment = Comment.objects.create(content=content,goods=goods,author=request.user)
        serizlize = CommentSerizlizer(comment)
        return restful.result(data=serizlize.data)
    else:
        return restful.params_error(message=form.get_errors())