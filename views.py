from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator

from logbook.models import Entry, Tag, User, Group
from logbook.forms import EntryForm

class UserEntryList(ListView):

    template_name = 'logbook/index.html'
    context_object_name = 'entries'

    def get_queryset(self):
        if (type(self.args[0]) == unicode):
            self.user = get_object_or_404(User, username=self.args[0])
        return self.user.entry_set.all().order_by('-timestamp')

class GroupEntryList(ListView):

    template_name = 'logbook/index.html'
    context_object_name = 'entries'

    def get_queryset(self):
        if (type(self.args[0]) == unicode):
            self.group = get_object_or_404(Group, name=self.args[0])
        return self.group.entry_set.all().order_by('-timestamp')

class TagEntryList(ListView):

    template_name = 'logbook/index.html'
    context_object_name = 'entries'

    def get_queryset(self):
        if (type(self.args[0]) == unicode):
            self.tag = get_object_or_404(Tag, name=self.args[0])
        return self.tag.entry_set.all().order_by('-timestamp')

class TagCreate(CreateView):
    model = Tag
    success_url = reverse_lazy('logbook:index')

class TagUpdate(UpdateView):
    model = Tag
    success_url = reverse_lazy('logbook:index')

class TagDelete(DeleteView):
    model = Tag
    success_url = reverse_lazy('logbook:index')

class EntryCreate(CreateView):
    form_class = EntryForm
    model = Entry
    success_url = reverse_lazy('logbook:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.timestamp = timezone.now()

        return super(EntryCreate, self).form_valid(form)

class EntryUpdate(UpdateView):
    model = Entry
    form_class = EntryForm
    success_url = reverse_lazy('logbook:index')

class EntryDelete(DeleteView):
    model = Entry
    success_url = reverse_lazy('logbook:index')

    def form_valid(self, form):
        if form.instance.submit == "Cancel":
            return False
        return super(EntryDelete, self).form_valid(form)
