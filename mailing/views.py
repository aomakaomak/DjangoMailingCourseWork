from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache

from django.shortcuts import render, get_object_or_404, redirect

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

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)


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

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)


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

class SendMailRunNowView(View):
    def post(self, request, pk):
        sendmail = get_object_or_404(SendMail, pk=pk)

        # если рассылка уже завершена – не даём запускать повторно
        if sendmail.status == SendMail.ENDED:
            return redirect('mailing:sendmail_detail', pk=sendmail.pk)

        # первый запуск – фиксируем старт
        if sendmail.status == SendMail.CREATED:
            sendmail.start()

        # отправляем письма всем получателям
        for client in sendmail.recipients.all():
            try:
                result = send_mail(
                    subject=sendmail.message.subject,
                    message=sendmail.message.text,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[client.email],
                    fail_silently=False,
                )

                if result:
                    attempt_status = MailingAttempt.SUCCESS
                    answer = 'Письмо успешно отправлено'
                else:
                    attempt_status = MailingAttempt.FAILED
                    answer = 'send_mail вернул 0 (письмо не отправлено)'

            except Exception as e:
                attempt_status = MailingAttempt.FAILED
                answer = str(e)

            MailingAttempt.objects.create(
                time_attempt=timezone.now(),
                status=attempt_status,
                answer=answer,
                sendmail=sendmail,
            )

        # фиксируем завершение рассылки
        sendmail.finish()

        return redirect('mailing:sendmail_detail', pk=sendmail.pk)

    def get(self, request, pk):
        # по GET не запускаем, просто редиректим на детали
        return redirect('mailing:sendmail_detail', pk=pk)


class IndexView(TemplateView):
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # всего рассылок
        context['total_sendmails'] = SendMail.objects.count()

        # активные рассылки (статус "запущена")
        context['active_sendmails'] = SendMail.objects.filter(
            status=SendMail.STARTED
        ).count()

        # уникальные получатели, которые вообще участвуют хотя бы в одной рассылке
        context['unique_clients'] = Client.objects.filter(
            sendmails__isnull=False
        ).distinct().count()

        return context


class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = 'mailing/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_sendmails = SendMail.objects.count()

        attempts_qs = MailingAttempt.objects.all()
        total_attempts = attempts_qs.count()
        success_attempts = attempts_qs.filter(status=MailingAttempt.SUCCESS).count()
        failed_attempts = attempts_qs.filter(status=MailingAttempt.FAILED).count()

        total_sent_messages = success_attempts

        context['total_sendmails'] = total_sendmails
        context['total_attempts'] = total_attempts
        context['success_attempts'] = success_attempts
        context['failed_attempts'] = failed_attempts
        context['total_sent_messages'] = total_sent_messages

        return context








