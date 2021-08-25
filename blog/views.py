from django.shortcuts import render
from .models import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.

def homepage(request):
    return render(request, 'blog/home.html')

class PostListView(generic.ListView):
    model = Post

class PostDetailView(generic.DetailView):
    model = Post


class PostDeleteView(generic.DeleteView):
    model = Post

class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'content', 'img']

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk':self.object.id})


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'content', 'img']
    

    def form_valid(self, form):
        self.post_object = form.save(commit=False)
        self.post_object.author = self.request.user.profile
        self.post_object.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk':self.post_object.id})