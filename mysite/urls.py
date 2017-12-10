"""mysite URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

polls_url = 'polls/'
contact_url = 'contacto/'
admin_url = 'admin/' 
main_url =  polls_url

def root_app(*peticion_http):
    return HttpResponseRedirect(main_url)

urlpatterns = [
    #url(r'^$', lambda peticion_http: HttpResponseRedirect(main_url)),
    url(r'^$', root_app),
    url(r'^{}'.format(polls_url), include('polls.urls')),
    url(r'^{}'.format(contact_url), include('contacto.urls')),
    url(r'^{}'.format(admin_url), admin.site.urls),
]

