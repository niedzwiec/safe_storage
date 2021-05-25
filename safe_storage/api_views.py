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
        urls = Storage.objects.filter(correct_usages__gt=0, file='').values('creation_date').annotate(
            Count('correct_usages'))
        files = Storage.objects.filter(correct_usages__gt=0, file__isnull=False).values('creation_date').annotate(
            Count('correct_usages'))
        d = {str(url.get('creation_date')):
                 {'filse': file['correct_usages__count'],
                  'links': url['correct_usages__count']}
             for url, file in zip(urls, files)}
        return Response(d)
