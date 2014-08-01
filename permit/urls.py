from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'permit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'permit_app.views.home', name='home'),
    url(r'^register/$', 'permit_app.views.register', name='register'),
    url(r'^profile/$', 'permit_app.views.profile', name='profile'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    #url(r'^password_reset_confirm/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$','django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^password_reset_complete/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
    url(r'^permit_application/$', 'permit_app.views.permit_application', name='permit_application'),
    url(r'^view_permits/$', 'permit_app.views.view_permits', name='view_permits'),
    url(r'^view_permit/(?P<permit_id>\w+)/$', 'permit_app.views.view_permit', name='view_permit'),
    url(r'^edit_permit/(?P<permit_id>\w+)/$', 'permit_app.views.edit_permit', name='edit_permit'),
    url(r'^test/$', 'permit_app.views.test', name='test'),
    url(r'^view_map/$', 'permit_app.views.view_map', name='view_map'),
    url(r'^view_map_info/$', 'permit_app.views.view_map_info', name='view_map_info'),
    url(r'^about/$', 'permit_app.views.about', name='about'),
    url(r'^charge/$', 'permit_app.views.charge', name='charge'),


    # url(r'^view_map/$', 'permit_app.views.view_map', name='view_map'),

)
