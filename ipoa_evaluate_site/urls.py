"""ipoa_evaluate_site URL Configuration

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
from django.contrib.auth.views import login
from account.views import logout
from evaluate.views import index, evaluate_article, evaluate_reply, all_evaluate_reply
    # non_evaluate_article, non_evaluate_reply, all_evaluate_article, all_evaluate_reply, all_no_evaluate_reply


urlpatterns = [
    url(r'^evaluate_article/$', evaluate_article),
    url(r'^evaluate_reply/(\d+)/$', evaluate_reply),

    # url(r'^non_evaluate_article/$', non_evaluate_reply),
    url(r'^evaluate_reply/$', all_evaluate_reply),
    # url(r'^all_evaluate_article/$', all_evaluate_article),
    # url(r'^all_evaluate_reply/$', all_evaluate_reply),
    # url(r'^all_no_evaluate_reply/$', all_no_evaluate_reply),

    url(r'^$', index),
    url(r'^accounts/login/$', login, name='login'),
    # url(r'^accounts/logout/$', logout),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^index/$', index, name='index'),
    url(r'^admin/', admin.site.urls),
]
