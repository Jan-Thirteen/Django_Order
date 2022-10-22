from django.urls import path
from . import views

app_name = 'cms'
urlpatterns = [
    path('',views.index,name='index'),
    path('goods_list/',views.NewsListView.as_view(),name='goods_list'),
    path('write_goods/',views.WriteGoodsView.as_view(),name='write_goods'),
    path('edit_goods/',views.EditNewsView.as_view(),name='edit_goods'),
    path('delete_goods/',views.delete_goods,name='delete_goods'),

    path('goods_category/',views.goods_category,name='goods_category'),
    path('add_goods_category/',views.add_goods_category,name='add_goods_category'),
    path('edit_goods_category/',views.edit_goods_category,name='edit_goods_category'),
    path('delete_goods_category/',views.delete_goods_category,name='delete_goods_category'),

    path('banners/',views.banners,name='banners'),
    path('banner_list/',views.banner_list,name='banner_list'),
    path('add_banner/',views.add_banner,name='add_banner'),
    path('delete_banner/',views.delete_banner,name='delete_banner'),
    path('edit_banner/',views.edit_banner,name='edit_banner'),

    path('upload_file/',views.upload_file,name='upload_file'),
    path('qntoken/',views.qntoken,name='qntoken')
]