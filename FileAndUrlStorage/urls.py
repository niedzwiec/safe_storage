"""FileAndUrlStorage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, reverse_lazy
from safe_storage import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url=reverse_lazy('login')), name='index'),
    path('accounts/', include('accounts.urls')),
    path('safe_storage/', include('safe_storage.urls')),
    path('download/media/<str:path>', views.Download.as_view(), name='download'),
    # path('auth/', include('djoser.urls.authtoken'))
]
