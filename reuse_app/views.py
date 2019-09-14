from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import auth

class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('email',) + UserCreationForm.Meta.fields

class Register(FormView):
    template_name = 'reuse_app/register.html'
    form_class = RegistrationForm
    success_url = '/'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return FormView.get(self, request)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class Login(FormView):
    template_name = 'reuse_app/login.html'
    form_class = AuthenticationForm
    success_url = '/'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return FormView.get(self, request)

    def form_valid(self, form):
        print(self.request)
        user = auth.authenticate(**form.cleaned_data)
        auth.login(self.request, user)
        #print(form.user)
        return super().form_valid(form)

def logout(request):
    auth.logout(request)
    return redirect('/')

def index(request):
    return HttpResponse('Hello there')
