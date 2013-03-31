from logbook.models import Tag

def logbook(request):
    ctx = { 'tags': Tag.objects.all() }
    return dict(logbook=ctx)
