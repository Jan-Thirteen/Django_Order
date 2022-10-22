from django.urls import path
from . import views

app_name = 'payinfo'

urlpatterns = [
    path('', views.index, name='index'),
    path('good_list/', views.good_list_view, name='good_list'),  # alipay测试
    path('check_html_view/', views.check_html_view, name='check_html_view/'),   # alipay测试
]