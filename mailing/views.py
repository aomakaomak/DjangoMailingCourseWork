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

from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class HelloWorld(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello World")

