from django.contrib import admin
from logbook.models import Entry, Tag


class TagInline(admin.TabularInline):
    model = Tag

class EntryAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,          {'fields': ['text', 'tag', 'user', 'group']}),
            ('Timestamp',   {'fields': ['timestamp'], 'classes': ['collapse']}),
            ]
            #inlines = (TagInline, )
    list_filter = ['timestamp']
    search_fields = ['test']
    date_hierarchy = 'timestamp'

admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag)
