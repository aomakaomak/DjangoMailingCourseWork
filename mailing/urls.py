from django.urls import path

from . import views
from .views import HelloWorld

from .views import ClientListView, ClientCreateView, ClientDetailView, ClientDeleteView, ClientUpdateView

app_name = 'mailing'

urlpatterns = [
    path('helloworld/', HelloWorld.as_view(), name='helloworld'),
    path('clients/', ClientListView.as_view(), name='clients_list'),
    path('clients/new/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
]