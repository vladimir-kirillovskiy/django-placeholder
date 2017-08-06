# howdy/urls.py
from django.conf.urls import url
from apifetch import views

urlpatterns = [
    url(r'^$', views.ApiPageView.as_view()),
    url(r'^users/(?P<user_id>[0-9]+)/$', views.UserPageView.as_view()),
    url(r'^users/(?P<user_id>[0-9]+)/posts/(?P<post_id>[0-9]+)$', views.PostPageView.as_view()),
    url(r'^export/(?P<user_id>[0-9]+)/$', views.ExportPage.as_view()),
    url(r'^getusers/$', views.GetUsersPageView.as_view()),
    url(r'^test/$', views.TestPageView.as_view()),
]
