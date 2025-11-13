from django.db import models

class Client(models.Model):
    email = models.EmailField(verbose_name='Почта', unique=True)
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')


class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name='Тема письма')
    text = models.TextField(verbose_name='Текст')



