from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from safe_storage.models import Storage


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ['file', 'url']


class StorageResponseSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=8, source='raw_password')

    class Meta:
        model = Storage
        fields = ['slug', 'password']

class StorageGetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ['url', 'file']
