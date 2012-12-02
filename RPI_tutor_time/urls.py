from django.conf.urls.defaults import patterns, include, url


import tutor_time.views
import django.contrib.auth.views
from django.contrib.auth.decorators import login_required

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
 
    url(r'^loginerror/', tutor_time.views.loginerror),
    url(r'^lookup/', login_required(tutor_time.views.lookup.as_view(), login_url='/loginerror')),
    url(r'^promote_user/', tutor_time.views.promote_user),
    url(r'^accounts/profile/', login_required(tutor_time.views.profile.as_view(), login_url='/loginerror')),
    url(r'^request_help/', login_required(tutor_time.views.request_help.as_view(), login_url='/loginerror'), name='request_help'),
    url(r'^claim_tutee/', login_required(tutor_time.views.claim_tutee.as_view(), login_url='/loginerror'), name='claim_tutee'),
    url(r'^create_account/', tutor_time.views.create_account.as_view()),
    url(r'^email_tutee/', login_required(tutor_time.views.emailTuteeView.as_view(), login_url='/loginerror')),
    url(r'^login/', django.contrib.auth.views.login, {'template_name': 'display_message.html', 'extra_context': {'message': 'Invalid user name or password', 'error': True}}),
    url(r'^logout/', tutor_time.views.logout_view.as_view()),
    url(r'^verify_account/([0-9a-z]+)', tutor_time.views.verify_account),
    url(r'^emails/([A-Za-z]+\.html)', tutor_time.views.show_emails.as_view()),
    url(r'^emails/', tutor_time.views.show_emails.as_view()),
    url(r'^$', tutor_time.views.index.as_view()),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
