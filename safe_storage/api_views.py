from django.db.models import Count
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from safe_storage.models import Storage
from safe_storage.serializer import StorageSerializer, StorageResponseSerializer


class StorageCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StorageSerializer

    def perform_create(self, serializer):
        self.object = serializer.save()

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        password = self.object.generate_password()
        self.object.save()
        self.object.raw_password = password
        serializer = StorageResponseSerializer(self.object)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetStorageLink(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        urls = Storage.objects.filter(correct_usages__gt=0, file='').order_by('creation_date').values(
            'creation_date').annotate(
            Count('correct_usages'))
        files = Storage.objects.filter(correct_usages__gt=0).exclude(file='').order_by('creation_date').values(
            'creation_date').annotate(
            Count('correct_usages'))

        d = {}
        for item in urls:
            d[item['creation_date']] = {'links': item['correct_usages__count'], 'files': 0}
        for item in files:
            date = item['creation_date']
            value = item['correct_usages__count']
            if date in d:
                d[date].update({'files': value})
            else:
                d[date] = {'files': value, 'links': 0}
        return Response(d)
