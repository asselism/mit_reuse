from django.core.exceptions import PermissionDenied
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import *

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

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return FormView.get(self, request)

    def form_valid(self, form):
        print(self.request)
        user = auth.authenticate(**form.cleaned_data)
        auth.login(self.request, user)

        url = self.request.GET.get('next', '/')
        return redirect(url)

class ListingCreate(LoginRequiredMixin, CreateView):
    model = Listing
    fields = ['title', 'loc_text', 'description']

    def form_valid(self, form):
        listing = form.save(commit = False)
        listing.user = self.request.user
        listing.save()
        return redirect('/')

class ListingUpdate(LoginRequiredMixin, UpdateView):
    model = Listing
    fields = ['title', 'loc_text', 'description']
    pk_url_kwarg = 'pk'
    success_url = '/'

    def get_object(self, queryset = None):
        listing = get_object_or_404(Listing,
            pk = self.kwargs.get(self.pk_url_kwarg, '')
        )
        user = self.request.user
        if user.is_superuser or listing.user == user:
            return listing
        else:
            raise PermissionDenied
           
class ListingView(DetailView):
    model = Listing
    context_object_name = 'listing'
    template_name = 'reuse_app/listing_view.html'

class ListingListUser(LoginRequiredMixin, ListView):
    model = Listing
    context_object_name = 'listings'
    template_name = 'reuse_app/listing_list.html'

    def get_queryset(self):
        return Listing.objects.filter(user = self.request.user)


class ListingList(ListView):
    model = Listing
    context_object_name = 'listings'
    template_name = 'reuse_app/listing_list.html'

def logout(request):
    auth.logout(request)
    return redirect('/')

def index(request):
    return HttpResponse('Hello there')
