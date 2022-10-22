from django.urls import path
from . import views

app_name = 'goods'
urlpatterns = [
    path('<int:goods_id>/', views.goods_detail, name='goods_detail'),
    path('list/',views.goods_list,name='goods_list'),
    path('public_comment/',views.public_comment,name='public_comment'),
]