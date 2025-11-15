from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

from django.shortcuts import render, get_object_or_404

from .models import Client, Message, SendMail, MailingAttempt

from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class HelloWorld(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello World")


class ClientCreateView(CreateView):
    model = Client
    fields = ('email', 'full_name', 'comment')
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:clients_list')


class ClientListView(ListView):
    model = Client
    template_name = 'mailing/clients_list.html'
    context_object_name = 'clients'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'mailing/client_detail.html'
    context_object_name = 'client'


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('email', 'full_name', 'comment')
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:clients_list')


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:clients_list')


