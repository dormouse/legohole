from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^discount/', views.discount, name='discount'),
    url(r'^search/$', views.search, name='search'),
    url(r'^(?P<set_id>[0-9]+)/$', views.detail, name='detail'),
]

