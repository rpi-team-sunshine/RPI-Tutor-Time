from django.conf.urls.defaults import patterns, include, url


from tutor_time.views
import django.contrib.auth.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'RPI_tutor_time.views.home', name='home'),
    # url(r'^RPI_tutor_time/', include('RPI_tutor_time.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #url(r'^create_account/', include('tutor_time.urls')),
	url(r'^accounts/profile/', tutor_time.views.profile),
    url(r'^request_help/', tutor_time.views.request_help, name='request_help'),
	url(r'^claim_tutee/', tutor_time.views.claim_tutee, name='claim_tutee'),
    url(r'^create_account/', tutor_time.views.create_account),
    url(r'^login/', django.contrib.auth.views.login),
    url(r'^logout/', tutor_time.views.logout_view),
    url(r'^$', tutor_time.views.index),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
