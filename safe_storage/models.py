import uuid
import string
import random
from django.db import models
from datetime import datetime


# Create your models here.
from django.urls import reverse
from django.utils import timezone


class Storage(models.Model):
    url = models.URLField(null=True, blank=True)
    password = models.CharField(max_length=8, null=True)
    slug = models.SlugField()
    file = models.FileField(null=True, blank=True, )
    creation_date = models.DateField(auto_now_add=True)
    correct_usages = models.IntegerField(default=0)

    def generate_password(self):
        password = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        self.password = hash(password)
        return password

    def check_password(self, password):
        return self.password == str(hash(password))

    def generate_url(self):
        self.slug = str(uuid.uuid4())
        return self.slug

    def get_absolute_url(self):
        return ""

    def is_active(self):
        return (timezone.now() - self.creation_date).days < 1

    def get_redirect_url(self):
        if self.file:
            return reverse('download', args=(self.file.name.split('/')[-1],))
        return self.url

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.slug is None or self.slug == "":
            self.generate_url()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return f"{self.url} {self.creation_date} {self.correct_usages}"
