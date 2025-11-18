from django.contrib import admin

from .models import Client, Message, SendMail, MailingAttempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "full_name",
    )
    list_filter = ("email",)
    search_fields = ("email",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "text",
    )
    list_filter = ("subject",)
    search_fields = (
        "subject",
        "text",
    )


@admin.register(SendMail)
class SendMailAdmin(admin.ModelAdmin):
    list_display = (
        "first_mailing",
        "last_mailing",
        "status",
    )
    list_filter = ("status",)
    search_fields = ("status",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = (
        "time_attempt",
        "status",
        "answer",
    )
    list_filter = ("time_attempt",)
    search_fields = ("answer",)
