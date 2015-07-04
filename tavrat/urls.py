from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tavrat.views.index'),
    url(r'^delete/(\d+)$', 'tavrat.views.delete'),

)
