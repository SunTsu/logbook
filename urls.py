from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from logbook.models import Entry, User, Group
from logbook import views
from logbook.views import UserEntryList, GroupEntryList, TagEntryList, EntryCreate, EntryDelete, EntryUpdate
from datetime import timedelta


urlpatterns = patterns('',
    url(r'^$', login_required(ListView.as_view(
        queryset=Entry.objects.all().order_by('-timestamp'),
        context_object_name='entries',
        template_name='logbook/index.html')),
        name='index'),
    url(r'^entry/bymonth/$', login_required(ListView.as_view(
        queryset=Entry.objects.filter(timestamp__year=timezone.now().year).order_by('-timestamp'),
        context_object_name='entries',
        template_name='logbook/index-by-month.html')),
        name='indexbymonth'),
    url(r'^entry/yearsbymonth/$', login_required(ListView.as_view(
        queryset=Entry.objects.all().order_by('-timestamp'),
        context_object_name='entries',
        template_name='logbook/index-years-by-month.html')),
        name='indexyearsbymonth'),
    url(r'^entry/bytag/$', login_required(ListView.as_view(
        queryset=Entry.objects.all().order_by('-timestamp'),
        context_object_name='entries',
        template_name='logbook/index-by-tag.html')),
        name='indexbytag'),
    url(r'^entry/byuser/$', login_required(ListView.as_view(
        queryset=Entry.objects.all().order_by('-timestamp'),
        context_object_name='entries',
        template_name='logbook/index-by-user.html')),
        name='indexbyuser'),
    url(r'^entry/bygroup/$', login_required(ListView.as_view(
        queryset=Entry.objects.all().order_by('-timestamp'),
        context_object_name='entries',
        template_name='logbook/index-by-group.html')),
        name='indexbygroup'),
    url(r'^entry/(?P<pk>\d+)/$',
        login_required(DetailView.as_view(
            model=Entry,
            template_name='logbook/detail.html')),
        name='detail'),
    url(r'^entry/add/$', login_required(EntryCreate.as_view()), name='entrycreate'),
    url(r'^entry/(?P<pk>\d+)/delete/$', login_required(EntryDelete.as_view()), name='entrydelete'),
    url(r'^entry/(?P<pk>\d+)/update/$', login_required(EntryUpdate.as_view()), name='entryupdate'),
    url(r'^entry/today/$', login_required(ListView.as_view(
        queryset=Entry.objects.filter(timestamp__gt=(timezone.now()-timedelta(days=1))).order_by('-timestamp'),
        context_object_name='entries',
        template_name='logbook/index.html')),
        name='indextoday'),
    url(r'^entry/yesterday/$', login_required(ListView.as_view(
        queryset=Entry.objects.filter(timestamp__gt=(timezone.now()-timedelta(days=2))).filter(timestamp__lt=(timezone.now()-timedelta(days=1))).order_by('-timestamp'),
        context_object_name='entries',
        template_name='logbook/index.html')),
        name='indexyesterday'),
    url(r'^entry/week/$', login_required(ListView.as_view(
        queryset=Entry.objects.filter(timestamp__gt=(timezone.now()-timedelta(days=7))).order_by('-timestamp'),
        context_object_name='entries',
        template_name='logbook/index.html')),
        name='indexweek'),
    url(r'^entry/month/$', login_required(ListView.as_view(
        queryset=Entry.objects.filter(timestamp__month=timezone.now().month).order_by('-timestamp'),
        context_object_name='entries',
        template_name='logbook/index.html')),
        name='indexmonth'),
    url(r'^entry/year/$', login_required(ListView.as_view(
        queryset=Entry.objects.filter(timestamp__year=timezone.now().year).order_by('-timestamp'),
        context_object_name='entries',
        template_name='logbook/index.html')),
        name='indexyear'),
    url(r'^user/(\w+)/$', login_required(UserEntryList.as_view()), name='user'),
    url(r'^group/(\w+)/$', login_required(GroupEntryList.as_view()), name='group'),
    url(r'^tag/(\w+)/$', login_required(TagEntryList.as_view()), name='tag'),
)
