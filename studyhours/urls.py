from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'studyhours.views.home', name='home'),
    #url(r'^studyhours/', include('studyhours.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^getPersonInfo/', 'hoursheet.views.searchPerson'),
    url(r'^signIn/', 'hoursheet.views.signIn'),
    url(r'^signOut/', 'hoursheet.views.signOut'),
    url(r'^index/', 'hoursheet.views.index'),
    url(r'^signedin/', 'hoursheet.views.viewSignedIn'),
    url(r'^weeks/(?P<week_id>\d+)/$', 'hoursheet.views.getWeekInfo'),
    url(r'^weeks/', 'hoursheet.views.weeks')
)
