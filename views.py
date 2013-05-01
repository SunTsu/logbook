from django.views.generic import ListView
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.views.generic import DetailView, ListView, FormView
from django.views.generic.dates import ArchiveIndexView, TodayArchiveView, DayArchiveView, WeekArchiveView, MonthArchiveView, YearArchiveView
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from datetime import timedelta

from logbook.models import Entry, Tag, User, Group
from logbook.forms import EntryForm, EntrySearchForm

class UserEntryList(ListView):
    "View Class that lists all Entries of a given User"

    template_name = 'logbook/index.html'
    context_object_name = 'entries'

    def get_queryset(self):
        if (type(self.args[0]) == unicode):
            self.user = get_object_or_404(User, username=self.args[0])
        return self.user.entry_set.all().order_by('-timestamp')

class GroupEntryList(ListView):
    "View Class that lists all Entries of a given Group"

    template_name = 'logbook/index.html'
    context_object_name = 'entries'

    def get_queryset(self):
        if (type(self.args[0]) == unicode):
            self.group = get_object_or_404(Group, name=self.args[0])
        return self.group.entry_set.all().order_by('-timestamp')

class TagEntryList(ListView):
    "View Class that lists all Entries having a certain Tag"

    template_name = 'logbook/index.html'
    context_object_name = 'entries'

    def get_queryset(self):
        if (type(self.args[0]) == unicode):
            self.tag = get_object_or_404(Tag, name=self.args[0])
        return self.tag.entry_set.all().order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super(TagEntryList, self).get_context_data(**kwargs)
        context['tag'] = self.tag
        return context

class MyIndexView():
    "View class that only sets defaults for Index views. Not to be used on it's own"

    num_latest = 5000
    allow_empty = True
    queryset=Entry.objects.all()
    date_field = 'timestamp'
    context_object_name='entries'
    template_name='logbook/index.html'
    make_object_list = True
    month_format = '%m'

class EntryIndex(MyIndexView, ArchiveIndexView):
    "Index view for Entries, latest first"

    def get_context_data(self, **kwargs):
        context = {
                'form': EntryForm(),
                }
        context.update(kwargs)
        return super(EntryIndex, self).get_context_data(**context)

class EntrySearchIndex(MyIndexView, FormView):
    template_name = 'logbook/entry_form.html'
    form_class = EntrySearchForm
    #def get(self, request, *args, **kwargs):
    def post(self, request, *args, **kwargs):
        post = text__contains=request.POST
        self.entries = Entry.objects.filter(text__contains=post['text']).order_by('-timestamp')

        #Get user and filter
        if post['user'] != u'':
            user = get_object_or_404(User, id=int(post['user']))
            self.entries = self.entries.filter(user_id=user.id)

        #Get group and filter
        if post['group'] != u'':
            group = get_object_or_404(Group, id=int(post['group']))
            self.entries = self.entries.filter(group_id=group.id)
        return render_to_response("logbook/index.html", {'entries': self.entries }, context_instance=RequestContext(request))

class EntryGroupBy(EntryIndex):
    "Group Entries by Tag, User, Group"

    def get_queryset(self):
        grouper = self.kwargs['grouper']
        self.template_name='logbook/index-by-%s.html' % (grouper)
        return Entry.objects.all().order_by('-timestamp')

class EntryIndexToday(MyIndexView, TodayArchiveView):
    "Today's Entries View"
    pass

class EntryIndexYesterday(MyIndexView, DayArchiveView):
    "Yesterday's Entries View"

    yesterday = (timezone.now()-timedelta(days=1))
    day = str(yesterday.day)
    month = str(yesterday.month)
    year = str(yesterday.year)

class EntryIndexThisWeek(MyIndexView, WeekArchiveView):
    "This week's Entries View"

    now = timezone.now()
    year = str(now.year)
    month = str(now.month)
    week = str((now-timedelta(days=now.weekday())).strftime("%U"))

class EntryIndexMonth(MyIndexView, MonthArchiveView):
    "Entries Index View for a given month"
    pass

class EntryIndexThisMonth(EntryIndexMonth):
    "This month's Entries View"

    now = timezone.now()
    year = str(now.year)
    month = str(now.month)

class EntryIndexThisYear(MyIndexView, YearArchiveView):
    "This year's Entries View"
    year = str(timezone.now().year)

class EntryDetails(DetailView):
    "Entry detail view"

    model=Entry
    template_name='logbook/detail.html'

class TagDetails(DetailView):
    "Tag detail view"

    model=Tag
    template_name='logbook/tag_details.html'

class TagCreate(CreateView):
    "Tag create form view"

    model = Tag
    success_url = reverse_lazy('logbook:index')

class TagUpdate(UpdateView):
    "Tag update form view"

    model = Tag
    success_url = reverse_lazy('logbook:index')

class TagDelete(DeleteView):
    "Tag delete form view"

    model = Tag
    success_url = reverse_lazy('logbook:index')

class EntryCreate(CreateView):
    "Entry create form view"

    form_class = EntryForm
    model = Entry
    success_url = reverse_lazy('logbook:index')

    def form_valid(self, form):
        "Add current User and timestamp values to new Entry"
        form.instance.user = self.request.user
        form.instance.timestamp = timezone.now()
        form.instance.changed_timestamp = timezone.now()

        return super(EntryCreate, self).form_valid(form)

class EntryUpdate(UpdateView):
    "Entry update form view"

    model = Entry
    form_class = EntryForm
    success_url = reverse_lazy('logbook:index')

    def form_valid(self, form):
        "Add changed timestamp to updated Entry"
        form.instance.changed_timestamp = timezone.now()

        return super(EntryUpdate, self).form_valid(form)

class EntryDelete(DeleteView):
    "Entry delete form view"
    model = Entry
    success_url = reverse_lazy('logbook:index')

    def form_valid(self, form):
        if form.instance.submit == "Cancel":
            return False
        return super(EntryDelete, self).form_valid(form)
