from accounts.models import Profile
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from .forms import SignupForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class SignupView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/signup.html'


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['pic']
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.profile
