from django.urls import path

from safe_storage import api_views
from safe_storage import views

urlpatterns = [
    path('', views.SafeStorageFormView.as_view(), name='add_to_storage'),
    path('<slug:slug>/', views.SafeStorageDetailView.as_view(), name='get_storage'),
    path('api/add_to_storage/', api_views.StorageCreateView.as_view(), name='api_add_to_storage'),
    path('api/get_storage/<slug:slug>/', api_views.GetStorageLink.as_view(), name='api_get_storage'),
    path('api/get_statistic/', api_views.GetStorageLink.as_view(), name='api_get_storage'),
]
