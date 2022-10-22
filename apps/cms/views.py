from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.http import require_POST,require_GET
from apps.goods.models import GoodsCategory,Goods,Banner
from utils import restful
from .forms import EditGoodsCategoryForm,WriteGoodsForm,AddBannerForm,EditBannerForm,EditGoodsForm
from django.core.paginator import Paginator


from django.contrib.admin.views.decorators import staff_member_required
# 限制员工、成员访问该路由，非员工访问跳转到index首页
@staff_member_required(login_url='index')
def index(request):
    return render(request,'cms/index.html')

from datetime import datetime
from django.utils.timezone import make_aware
from urllib import parse    # 将参数转变为url查询字符串
class NewsListView(View):
    def get(self,request):
        # request.GET：获取出来的所有数据，都是字符串类型
        page = int(request.GET.get('p',1))  # 如果没有p，默认值为1
        # start = request.GET.get('start')
        # end = request.GET.get('end')
        name = request.GET.get('name')
        # request.GET.get(参数,默认值)
        # 这个默认值是只有这个参数没有传递的时候才会使用
        # 如果传递了，但是是一个空的字符串，那么也不会使用默认值
        category_id = int(request.GET.get('category',0) or 0)

        goods = Goods.objects.select_related('category')

        # if start or end:    # 判断是否提交了开始、结束日期
        #     if start:
        #         start_date = datetime.strptime(start,'%Y/%m/%d')
        #     else:
        #         start_date = datetime(year=2018,month=6,day=1)
        #     if end:
        #         end_date = datetime.strptime(end,'%Y/%m/%d')
        #     else:
        #         end_date = datetime.today()
        #     newses = newses.filter(pub_time__range=(make_aware(start_date),make_aware(end_date)))

        if name:   # 是否有标题
            goods = goods.filter(title__icontains=name)

        if category_id:     # 按分类查询
            goods = goods.filter(category=category_id)

        paginator = Paginator(goods, 2)
        page_obj = paginator.page(page)

        context_data = self.get_pagination_data(paginator,page_obj)

        context = {
            'categories': GoodsCategory.objects.all(),
            'goods': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            # 'start': start,
            # 'end': end,
            'name': name,
            'category_id': category_id,
            'url_query': '&'+parse.urlencode({  # 查询参数
                # 'start': start or '',
                # 'end': end or '',
                'name': name or '',
                'category': category_id or ''
            })
        }

        print('='*30)
        print(category_id)
        print('='*30)

        context.update(context_data)

        return render(request, 'cms/news_list.html', context=context)


    def get_pagination_data(self,paginator,page_obj,around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1,current_page)
        else:
            left_has_more = True
            left_pages = range(current_page-around_count,current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page+1,num_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_page+1,current_page+around_count+1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


class WriteGoodsView(View):
    def get(self,request):
        categories = GoodsCategory.objects.all()
        context = {
            'categories': categories
        }
        return render(request,'cms/write_news.html',context=context)

    def post(self,request):
        form = WriteGoodsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            # desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = GoodsCategory.objects.get(pk=category_id)
            price = form.cleaned_data.get('price')
            Goods.objects.create(name=name,thumbnail=thumbnail,content=content,category=category,price=price) # ,author=request.user
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())

class EditNewsView(View):
    def get(self,request):
        goods_id = request.GET.get('goods_id')
        goods = Goods.objects.get(pk=goods_id)
        print('='*30)
        print(goods_id)
        print('='*30)
        context = {
            'goods': goods,
            'categories': GoodsCategory.objects.all()
        }
        return render(request,'cms/write_news.html',context=context)

    def post(self,request):
        form = EditGoodsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            # desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            pk = form.cleaned_data.get("pk")
            price = form.cleaned_data.get("price")
            category = GoodsCategory.objects.get(pk=category_id)
            Goods.objects.filter(pk=pk).update(name=name,thumbnail=thumbnail,content=content,category=category,price=price)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_errors())

@require_POST
def delete_goods(request):
    goods_id = request.POST.get('goods_id')
    Goods.objects.filter(pk=goods_id).delete()
    return restful.ok()

from django.db.models import Count
@require_GET
def goods_category(request):
    categories = GoodsCategory.objects.all()
    # result = Goods.objects.values("category_id").annotate(num=Count('category_id'))
    result = GoodsCategory.objects.annotate(num_count=Count("goods"))
    print("##" * 20)
    print(result)
    for a in result:
        print("%d,%d",(a.pk,a.name,a.num_count))
    for cate in categories:
        print("pk=%d name=%s" % (cate.pk, cate.name))
    context = {
        'categories': categories,
        'result': result
    }
    # print(categories)
    return render(request,'cms/news_category.html',context=context)


@require_POST
def add_goods_category(request):
    name = request.POST.get('name')
    exists = GoodsCategory.objects.filter(name=name).exists()
    if not exists:
        GoodsCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message='该分类已经存在！')


@require_POST
def edit_goods_category(request):
    form = EditGoodsCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            GoodsCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except:
            return restful.params_error(message='该分类不存在！')
    else:
        return restful.params_error(message=form.get_error())


@require_POST
def delete_goods_category(request):
    pk = request.POST.get('pk')
    try:
        GoodsCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.unauth(message='该分类不存在！')

def banners(request):
    return render(request,'cms/banners.html')

from apps.goods.serializers import BannerSerializer
def banner_list(request):
    banners = Banner.objects.all()
    serialize = BannerSerializer(banners,many=True)
    return restful.result(data=serialize.data)


def add_banner(request):
    form = AddBannerForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        banner = Banner.objects.create(priority=priority,image_url=image_url,link_to=link_to)
        return restful.result(data={"banner_id":banner.pk})
    else:
        return restful.params_error(message=form.get_errors())

def delete_banner(request):
    banner_id = request.POST.get('banner_id')
    Banner.objects.filter(pk=banner_id).delete()
    return restful.ok()


def edit_banner(request):
    form = EditBannerForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        priority = form.cleaned_data.get('priority')
        Banner.objects.filter(pk=pk).update(image_url=image_url,link_to=link_to,priority=priority)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())


import os
from django.conf import settings
@require_POST
def upload_file(request):
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT,name),'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL+name)   # 返回图片再服务器中的完整路径
    # http://127.0.1:8000/media/abc.jpg
    return restful.result(data={'url':url})

import qiniu
@require_GET
def qntoken(request):
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SECRET_KEY

    bucket = settings.QINIU_BUCKET_NAME
    q = qiniu.Auth(access_key,secret_key)

    token = q.upload_token(bucket)

    return restful.result(data={"token":token})