from django.urls import re_path
from . import views
urlpatterns = [
    re_path(r'^$', views.base_view, name='home'),
    re_path(r'^cart/$', views.cart, name='cart'),
    re_path(r'^account/$', views.account, name='account'),
    re_path(r'^checkout/$', views.checkout, name='checkout'),
    re_path(r'^order/$', views.order, name='create_order'),
    re_path(r'^thank_you/$', views.thank_you, name='thank_you'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^logout/$', views.logout, name='logout'),
    re_path(r'^product/(?P<product_id>[-\d]+)/$', views.product_detail, name='product_detail'),
    re_path(r'^add_to_cart/(?P<id>[-\d]+)/$', views.add_to_cart, name='add_to_cart'),
    re_path(r'^remove_from_cart/(?P<item_id>[-\d]+)/$', views.remove_from_cart, name='remove_from_cart'),
    re_path(r'^edit_cart_item/$', views.edit_cart_item, name='edit_cart_item'),
    re_path(r'^category/(?P<category_slug>[-\w]+)/$', views.products_by_category, name='category_detail'),
]
