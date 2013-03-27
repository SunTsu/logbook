from django import forms
from logbook.models import Entry, Tag, User, Group

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ('user', 'timestamp',)
