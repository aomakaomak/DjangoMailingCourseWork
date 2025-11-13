from django.urls import path

from . import views
from .views import HelloWorld

# from .views import

app_name = 'mailing'

urlpatterns = [
    path('helloworld/', HelloWorld.as_view(), name='helloworld'),
]