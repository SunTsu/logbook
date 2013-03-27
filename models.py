from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField('tag', max_length=20)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Entry(models.Model):
    timestamp = models.DateTimeField('Date published',default=timezone.now())
    text = models.TextField('log entry', max_length=5000)
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    tag = models.ManyToManyField(Tag, blank=True, null=True)

    def entered_today(self):
        return self.timestamp.date() == timezone.now().date()

    def entered_this_month(self):
        return self.timestamp.month == timezone.now().month

    def entered_this_year(self):
        return self.timestamp.year == timezone.now().year

    def entered_during_seven_days(self):
        return (timezone.now()-self.timestamp).days < 7

    def get_tag_display(self):
        tags = Tag.objects.all()
        tag_display = [tag.name for tag in tags]
        return tag_display

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ('timestamp',)

