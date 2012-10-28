from django.conf.urls.defaults import patterns, url

from tutor_time import views

urlpatterns = patterns('',
    url(r'^claim_tutee/', views.claim_tutee, name='claim_tutee'),
    url(r'^create_account/', views.create_account, name='create account'),
    url(r'^$', views.index, name='index'),
)
