from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.list import ListView
from mit_reuse.settings import MAPS_API_KEY

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
        user = auth.authenticate(**form.cleaned_data)
        auth.login(self.request, user)

        url = self.request.GET.get('next', '/')
        return redirect(url)

listing_fields = ('title', 'loc_text', 'description', 'loc_lat', 'loc_lng')

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'loc_text', 'description', 'loc_lat', 'loc_lng')
        widgets = {
            'loc_lat': forms.HiddenInput(),
            'loc_lng': forms.HiddenInput()
        }

class ListingCreate(LoginRequiredMixin, CreateView):
    model = Listing
    #fields = listing_fields
    form_class = ListingForm
    extra_context = {
        'submit_value': 'Create Listing',
        'MAPS_API_KEY': MAPS_API_KEY
    }

    def form_valid(self, form):
        listing = form.save(commit = False)
        listing.user = self.request.user
        listing.save()
        return redirect('reuse_app:listing_view', listing.pk)

def get_listing_or_403(view):
    listing = get_object_or_404(Listing,
        pk = view.kwargs.get('pk', '')
    )
    user = view.request.user
    if user.is_superuser or listing.user == user:
        return listing
    else:
        raise PermissionDenied

class ListingUpdate(LoginRequiredMixin, UpdateView):
    model = Listing
    form_class = ListingForm
    extra_context = {
        'submit_value': 'Update Listing',
        'MAPS_API_KEY': MAPS_API_KEY
    }

    def get_object(self, queryset = None):
        return get_listing_or_403(self)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs.get(self.pk_url_kwarg, '')
        return context

    def get_success_url(self):
        return reverse(
            'reuse_app:listing_view',
            args=[self.kwargs.get(self.pk_url_kwarg, '')]
        )

class ListingDelete(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        self.kwargs = kwargs
        self.request = request

        listing = get_listing_or_403(self)
        listing.delete()

        return redirect('reuse_app:listings_list_user')

class ListingView(DetailView):
    model = Listing
    context_object_name = 'listing'
    template_name = 'reuse_app/listing_view.html'
    extra_context = {
        'MAPS_API_KEY': MAPS_API_KEY
    }

class ListingTaken(LoginRequiredMixin, ListingView):
    template_name = 'reuse_app/listing_taken.html'

    def post(self, request, pk):
        listing = get_object_or_404(Listing, pk = pk)
        listing.marked_taken = True
        listing.save()
        return redirect('reuse_app:listing_view', pk)
    

class ListingListUser(LoginRequiredMixin, ListView):
    model = Listing
    context_object_name = 'listings'
    template_name = 'reuse_app/listing_list.html'

    def get_queryset(self):
        return Listing.objects.filter(user = self.request.user)

class ListingList(ListView):
    model = Listing
    context_object_name = 'listings'
    template_name = 'reuse_app/listing_map.html'
    extra_context = {
        'MAPS_API_KEY': MAPS_API_KEY
    }

def logout(request):
    auth.logout(request)
    return redirect('/')

def index(request):
    return HttpResponse('Hello there')
