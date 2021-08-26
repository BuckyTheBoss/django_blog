from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
# Create your views here.

def homepage(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You are not logged in')
    else:
        messages.success(request, 'Welcome back to the homepage')

    return render(request, 'blog/home.html')


class PostListView(generic.ListView):
    model = Post


class PostDeleteView(generic.DeleteView):
    model = Post


class PostUpdateView(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'content', 'img']
    success_message = 'You\'ve successfully edited your post'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk':self.object.id})

    def form_invalid(self, form):
        messages.error(self.request, 'you messed up with that form')
        return super().form_invalid(form)

    def get_queryset(self):
        qs = super().get_queryset()
        print('original qs', qs)
        filtered_qs = qs.filter(author=self.request.user.profile)
        print('filtered qs', filtered_qs)
        return filtered_qs


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


class PostDetailView(generic.DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            
            return redirect('post_comment', kwargs['pk'])
        return super().get(request, *args, **kwargs)




class CommentCreateView(generic.CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/post_detail.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('post_detail', kwargs['pk'])
        return super().get(request, *args, **kwargs)

    def get_post(self):
        post_id = self.kwargs['pk']
        return get_object_or_404(Post, id=post_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_post()
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user.profile
        comment.post = self.get_post()
        comment.save()
        return redirect('post_detail', comment.post.id)

class CommentEditView(generic.UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk':self.object.post.id})

    def get_queryset(self):
        qs = super().get_queryset()
        filtered_qs = qs.filter(author=self.request.user.profile)
        return filtered_qs


def search_results(request):
    query = request.GET.get('search')
    results = Post.objects.filter(
        Q(title__contains=query) |
        Q(content__contains=query)
    )

    return render(request, 'blog/search.html', {'q':query, 'results': results})
