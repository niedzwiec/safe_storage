import os
from datetime import date

from django.core.wsgi import get_wsgi_application
from django.db.models import Count

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FileAndUrlStorage.settings")
application = get_wsgi_application()

from safe_storage.models import Storage


# for x in range(20):
#     s = Storage.objects.create(file=f"wp{x}.pl")
#     s.creation_date = date(2020, 1, x+1)
#     s.correct_usages = x%10
#     s.save()

urls = Storage.objects.filter(correct_usages__gt=0, file='').order_by('creation_date').values('creation_date').annotate(
            Count('correct_usages'))
files = Storage.objects.filter(correct_usages__gt=0).exclude(file='').order_by('creation_date').values('creation_date').annotate(
            Count('correct_usages'))

print(urls)
print(files)