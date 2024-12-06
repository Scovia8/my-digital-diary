

from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm
from .models import Comment

# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html', {'title': "About Page"})


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]

class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    form_class = CommentForm
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['comments'] = Comment.objects.filter(post=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():

            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):

        return redirect(self.object.get_absolute_url())



def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = Post.objects.filter(active=True)
    new_comments = None
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comments = comment_form.save(commit=False)
            new_comments.post = post
            new_comments.save()
    else:
        comment_form = CommentForm()
    return render(request, template_name, {'post': post, 'comments': comments, 'comment_form': comment_form, "new_comments" : new_comments})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'
    template_name = 'post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# API Views


# Create your views here.
