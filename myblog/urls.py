from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.graph, name='graph'),
    url(r'^api/get_data/$', views.get_data, name='get_data'),
    url(r'^api/get_data/(?P<num_items>[0-9]+)', views.get_data, name='get_data'),
    url(r'^all/$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
]