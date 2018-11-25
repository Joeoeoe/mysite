from django.urls import re_path
from blogApp import views

urlpatterns = [
    re_path(r'^test_view/$', views.test_view),
    re_path(r'^login_view/$', views.login_view),
    re_path(r'^logout_view/$', views.logout_view),
    re_path(r'^is_logined_view/$', views.is_logined_view),
    re_path(r'^is_token_valid/$', views.is_token_valid),
    re_path(r'^post_blog_view/$', views.post_blog_view),
    re_path(r'^get_blogByID_view/$', views.get_blogByID_view),
    re_path(r'^get_blogList_view/$', views.get_blogList_view),
    re_path(r'^get_blogList_recently_view/$', views.get_blogList_recently_view),
    re_path(r'^delete_blog_view/$', views.delete_blog_view),
    re_path(r'^edit_blog_view/$', views.edit_blog_view)
]


