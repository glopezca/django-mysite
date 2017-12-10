from django.conf.urls import url
from django.urls import reverse

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    ##url(r'^$', views.index, name='index'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    ##url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    ##url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    ##url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.QuestionDelete.as_view(), name='delete'),
    
    ### Distinas formas equivalentes de crear preguntas:

    url(r'^create/$', views.QuestionCreate.as_view(), name='create'), # Forma recomendada
    #url(r'^create/$', views.crea_pregunta1, name='create'),
    #url(r'^create/$', views.crea_pregunta2, name='create'),
]