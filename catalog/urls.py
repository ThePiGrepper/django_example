from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^now/$', views.timenow),
]
