from django.db import models
from django.utils import timezone
from django.conf import settings


class Client(models.Model):
    email = models.EmailField(verbose_name="Почта", unique=True)
    full_name = models.CharField(max_length=150, verbose_name="ФИО")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clients",
        verbose_name="Владелец",
    )

    def __str__(self):
        return self.email

    class Meta:
        permissions = [
            ("view_all_clients", "Может просматривать всех клиентов"),
        ]


class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name="Тема письма")
    text = models.TextField(verbose_name="Текст")

    def __str__(self):
        return self.subject


class SendMail(models.Model):

    CREATED = "created"
    STARTED = "started"
    ENDED = "ended"

    SENDMAIL_STATUS_CHOICES = [
        (CREATED, "создана"),
        (STARTED, "запущена"),
        (ENDED, "завершена"),
    ]

    first_mailing = models.DateTimeField(
        verbose_name="Дата и время первой отправки", blank=True, null=True
    )
    last_mailing = models.DateTimeField(
        verbose_name="Дата и время окончания отправки", blank=True, null=True
    )
    status = models.CharField(
        max_length=8,
        choices=SENDMAIL_STATUS_CHOICES,
        default=CREATED,
        verbose_name="Статус",
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="sendmails",
        verbose_name="Сообщение",
    )
    recipients = models.ManyToManyField(
        Client, related_name="sendmails", verbose_name="Получатели"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sendmails",
        verbose_name="Владелец",
    )

    def __str__(self):
        return f"Рассылка: {self.message.subject}"

    def start(self):
        self.first_mailing = timezone.now()
        self.status = self.STARTED
        self.save()

    def finish(self):
        self.last_mailing = timezone.now()
        self.status = self.ENDED
        self.save()

    class Meta:
        permissions = [
            ("view_all_sendmails", "Может просматривать все рассылки"),
            ("disable_sendmail", "Может отключать рассылки"),
        ]


class MailingAttempt(models.Model):
    SUCCESS = "success"
    FAILED = "failed"

    ATTEMPT_STATUS_CHOICES = [
        (SUCCESS, "успешно"),
        (FAILED, "не успешно"),
    ]

    time_attempt = models.DateTimeField(verbose_name="Дата и время попытки отправки")
    status = models.CharField(
        max_length=8, choices=ATTEMPT_STATUS_CHOICES, verbose_name="Статус"
    )
    answer = models.TextField(verbose_name="Ответ почтового сервиса")
    sendmail = models.ForeignKey(
        SendMail,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Рассылка",
    )
