from django.urls import path

from . import views
from .views import HelloWorld

from .views import ClientListView, ClientCreateView, ClientDetailView, ClientDeleteView, ClientUpdateView, MessageDeleteView, MessageUpdateView, MessageCreateView, MessageDetailView, MessageListView, SendMailDeleteView, SendMailDetailView, SendMailUpdateView, SendMailCreateView, SendMailListView, SendMailRunNowView, IndexView

app_name = 'mailing'

urlpatterns = [
    path('helloworld/', HelloWorld.as_view(), name='helloworld'),
    path('clients/', ClientListView.as_view(), name='clients_list'),
    path('clients/new/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('messages/', MessageListView.as_view(), name='messages_list'),
    path('messages/new/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('sendmails/',SendMailListView.as_view(), name='sendmails_list'),
    path('sendmails/new/', SendMailCreateView.as_view(), name='sendmail_create'),
    path('sendmails/<int:pk>/', SendMailDetailView.as_view(), name='sendmail_detail'),
    path('sendmails/update/<int:pk>/', SendMailUpdateView.as_view(), name='sendmail_update'),
    path('sendmails/delete/<int:pk>/', SendMailDeleteView.as_view(), name='sendmail_delete'),

    path('sendmails/run_now/<int:pk>/', SendMailRunNowView.as_view(), name='sendmail_run_now'),

    path('index/', IndexView.as_view(), name='index')
]