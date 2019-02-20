"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^register/$',views.register,name='register'),
    url(r'^register_handle/$',views.register_handle,name='register_handle'),
    url(r'^login/$',views.login,name='login'),
    url(r'^login_check/$',views.login_check,name='login_check'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^$',views.user,name='user'),
    url(r'^address/$',views.address,name='address'),
    url(r'^order/(?P<page>\d+)?/?$', views.order, name='order'),
    url(r'^verifycode/$',views.verifyocde,name='verifycode'),
    url(r'^active/(?P<token>.*)/$',views.register_active,name='active'),

]
