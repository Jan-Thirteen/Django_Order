from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_index, name='cart_index'),
    path('add_cart/', views.add_cart, name='add_cart'),
    path('delete_cart/', views.delete_cart, name='delete_cart'),
    path('check_out/', views.check_out, name='check_out'),
    path('check_html_view/', views.check_html_view, name='check_html_view'),
    # path('<int:course_id>/', views.course_detail, name='course_detail'),
    # path('course_token/', views.course_token, name='course_token'),
    # path('course_order/<int:course_id>/', views.course_order, name='course_order'),
    # path('course_order_key/', views.course_order_key, name="course_order_key"),
    # path('notify_view/', views.notify_view, name='notify_view')
]
