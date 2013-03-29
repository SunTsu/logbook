from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from logbook.models import Entry, User, Group
from logbook import views
from logbook.views import *
from datetime import timedelta


urlpatterns = patterns('',
    url(r'^$', login_required(EntryIndex.as_view()), name='index'),
    url(r'^entry/groupby/(?P<grouper>\w+)/$', login_required(EntryGroupBy.as_view()), name='indexby'),
    url(r'^entry/(?P<pk>\d+)/$', login_required(EntryDetails.as_view()), name='detail'),
    url(r'^entry/add/$', login_required(EntryCreate.as_view()), name='entrycreate'),
    url(r'^entry/(?P<pk>\d+)/delete/$', login_required(EntryDelete.as_view()), name='entrydelete'),
    url(r'^entry/(?P<pk>\d+)/update/$', login_required(EntryUpdate.as_view()), name='entryupdate'),
    url(r'^entry/today/$', login_required(EntryIndexToday.as_view()), name='indextoday'),
    url(r'^entry/yesterday/$', login_required(EntryIndexYesterday.as_view()), name='indexyesterday'),
    url(r'^entry/week/$', login_required(EntryIndexThisWeek.as_view()), name='indexweek'),
    url(r'^entry/month/$', login_required(EntryIndexThisMonth.as_view()), name='indexmonth'),
    url(r'^entry/year/$', login_required(EntryIndexThisYear.as_view()), name='indexyear'),
    url(r'^user/(\w+)/$', login_required(UserEntryList.as_view()), name='user'),
    url(r'^group/(\w+)/$', login_required(GroupEntryList.as_view()), name='group'),
    url(r'^tag/add/$', login_required(TagCreate.as_view()), name='tagcreate'),
    url(r'^tag/(?P<pk>\d+)/details/$', login_required(TagDetails.as_view()), name='tagdetail'),
    url(r'^tag/(?P<pk>\d+)/delete/$', login_required(TagDelete.as_view()), name='tagdelete'),
    url(r'^tag/(?P<pk>\d+)/update/$', login_required(TagUpdate.as_view()), name='tagupdate'),
    url(r'^tag/(\w+)/$', login_required(TagEntryList.as_view()), name='tag'),
)
