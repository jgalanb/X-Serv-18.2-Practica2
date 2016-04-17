from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^/?$', 'practica2.views.recurso_barra'),
    url(r'/?(\d+)$', 'practica2.views.recurso_redirect'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'.*', 'practica2.views.error'),
)
