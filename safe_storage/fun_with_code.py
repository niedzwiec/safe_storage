import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FileAndUrlStorage.settings')
import django
django.setup()
from datetime import datetime, date
# from django.conf import settings
# settings.configure()

from django.db.models import Q, Count, Sum
from safe_storage.models import Storage
#
# for x in range(1,10):
#     s = Storage()
#     s.url=f'wp{x}.pl'
#     s.file = 'ala_ma_jota'
#     s.correct_usages= x%3+1
#     s.save()
#     s.creation_date = datetime(year=2000, month=1, day=x)
#     s.save()



s =  Storage.objects.filter(correct_usages__gt=0, file='').values('creation_date').annotate(Sum('correct_usages'))
s1 = Storage.objects.filter(correct_usages__gt=0, file__isnull=False).values('creation_date').annotate(Sum('correct_usages'))
d = {
}
for url, file in zip(s, s1):
    d[str(url.get('creation_date'))] = {
        'filse': file['correct_usages__sum'],
        'links': url['correct_usages__sum'],
    }
print(d)