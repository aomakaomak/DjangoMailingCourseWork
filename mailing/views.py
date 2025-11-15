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


class MessageCreateView(CreateView):
    model = Message
    fields = ('subject', 'text', )
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages_list')


class MessageListView(ListView):
    model = Message
    template_name = 'mailing/messages_list.html'
    context_object_name = 'messages'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('subject', 'text',)
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:messages_list')


class SendMailCreateView(CreateView):
    model = SendMail
    fields = ('message', 'recipients', )
    template_name = 'mailing/sendmail_form.html'
    success_url = reverse_lazy('mailing:sendmails_list')


class SendMailListView(ListView):
    model = SendMail
    template_name = 'mailing/sendmails_list.html'
    context_object_name = 'sendmails'


class SendMailDetailView(DetailView):
    model = SendMail
    template_name = 'mailing/sendmail_detail.html'
    context_object_name = 'sendmail'


class SendMailUpdateView(UpdateView):
    model = SendMail
    fields = ('message', 'recipients',)
    template_name = 'mailing/sendmail_form.html'
    success_url = reverse_lazy('mailing:sendmails_list')


class SendMailDeleteView(DeleteView):
    model = SendMail
    template_name = 'mailing/sendmail_confirm_delete.html'
    success_url = reverse_lazy('mailing:sendmails_list')






