from django import forms
from logbook.models import Entry, Tag, User, Group

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ('user', 'changed_timestamp')

class EntrySearchForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ('tag', 'timestamp', 'changed_timestamp')
