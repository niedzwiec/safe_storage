from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from safe_storage.models import Storage


class CheckPasswordForm(forms.Form):
    slug = forms.CharField(widget=forms.HiddenInput())
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        data = super().clean()
        try:
            Storage.objects.get(slug=data['slug'], password=hash(data['password']))
        except ObjectDoesNotExist:
            raise ValidationError('Incorrect Password')


class StorageModelForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = ['file', 'url']

    def clean(self):
        data = super().clean()
        file = data.get('file', '')
        if file is None:
            file = ''
        url = data.get('url', '')
        if url is None:
            url = ''
        if file == '' and url == '':
            raise ValidationError("You mast give one of them")
        if file != '' and url != '':
            raise ValidationError("You can only pass one of them")
