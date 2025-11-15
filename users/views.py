from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.mail import send_mail
from .forms import CustomUserCreationForm

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

from .tokens import email_verification_token
from .models import CustomUser

from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages

from .tokens import email_verification_token

User = get_user_model()


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('mailing:index')

    def form_valid(self, form):
        # сохраняем пользователя ОДИН раз, явно
        user: CustomUser = form.save(commit=False)
        user.is_active = False
        user.save()

        self.object = user  # чтобы CreateView знал, какой объект создан
        self.send_verification_email(user)

        return redirect(self.get_success_url())

    def send_verification_email(self, user: CustomUser):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = email_verification_token.make_token(user)

        activation_link = self.request.build_absolute_uri(
            reverse_lazy('users:activate', kwargs={'uidb64': uid, 'token': token})
        )

        subject = 'Подтверждение email'
        message = f'Для подтверждения email перейдите по ссылке:\n{activation_link}'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist):
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Ваш email подтверждён, вы вошли в систему.')
        return redirect('mailing:index')
    else:
        return render(request, 'users/activation_invalid.html')


