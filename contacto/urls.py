# Fichero de las URLs de la aplicación "encuestas"

from django.conf.urls import url

from . import views

app_name = "contacto"
urlpatterns = [
    url(r'^$', views.ContactView.contacto, name="contacto"),
    url(r'^gracias/$', views.ContactView.gracias, name="gracias")
]