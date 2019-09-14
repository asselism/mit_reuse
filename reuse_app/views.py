from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import auth

class Register(FormView):
    template_name = 'reuse_app/register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class Login(FormView):
    template_name = 'reuse_app/login.html'
    form_class = AuthenticationForm
    success_url = '/'

    def form_valid(self, form):
        print(self.request)
        user = auth.authenticate(**form.cleaned_data)
        auth.login(self.request, user)
        #print(form.user)
        return super().form_valid(form)

def index(request):
    return HttpResponse('Hello there')
