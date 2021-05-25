import os

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, FormView

from safe_storage.forms import StorageModelForm, CheckPasswordForm
from safe_storage.models import Storage


class SafeStorageFormView(LoginRequiredMixin, CreateView):
    template_name = 'form_view.html'
    response_template_name = 'safe_storage/storage_detail.html'
    form_class = StorageModelForm

    def form_valid(self, form):
        super().form_valid(form)
        password = self.object.generate_password()
        self.object.generate_url()
        self.object.save()
        return render(self.request, self.response_template_name, {'storage': self.object, 'password': password})


class SafeStorageDetailView(FormView):
    template_name = 'form_view.html'
    form_class = CheckPasswordForm
    success_url = "/"

    def get_initial(self):
        initial = super().get_initial()
        initial['slug'] = self.kwargs['slug']
        return initial

    def form_valid(self, form):
        super().form_valid(form)
        storage = Storage.objects.get(slug=self.kwargs['slug'])
        if not storage.is_active():
            return HttpResponse("Link outdated")
        storage.correct_usages += 1
        storage.save()
        return render(self.request, 'safe_storage/detail_view.html',
                      {'storage': storage})


class Download(View):
    def get(self, request, path):
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
