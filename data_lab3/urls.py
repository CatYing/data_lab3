"""data_lab3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from lab3 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^any/$', views.AnyView.as_view(), name='any'),
    url(r'^level/create/$', views.LevelCreateView.as_view(), name='level-create'),
    url(r'^level/update/$', views.LevelUpdateView.as_view(), name='level-update'),
    url(r'^level/delete/', views.delete_level, name='level-delete'),
    url(r'^user/list/$', views.UserListView.as_view(), name='user-list'),
    url(r'^user/friends/(?P<pk>.*)/$', views.UserFriendsListView.as_view(), name='user-friends'),
    url(r'^edu/mix/$', views.UserEducationMixView.as_view(), name='edu-mix'),
    url(r'^edu.group/$', views.UserEducationGroupView.as_view(), name='edu-group'),

    url(r'^api/any/$', views.api_query_any, name='api-any'),

]
