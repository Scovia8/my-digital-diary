from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm, ReplyForm, PostForm
from .models import Comment, BlogPost


def latest_posts(request):
    posts = BlogPost.objects.order_by('-created_at')[:3]
    print(f"Latest Posts: {latest_posts}")
    return render(request, 'home.html', {'posts': posts})


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog-detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html', {'title': "About Page"})


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()  # Use one form for both comments and replies
        context['comments'] = Comment.objects.filter(post=self.object, parent=None)  # Only top-level comments
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        form = CommentForm(request.POST, request.FILES)  # Handle file uploads for comments
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.name = request.user.username  # or however you identify users
            parent_id = request.POST.get('parent_id')  # Check for parent comment ID
            if parent_id:
                comment.parent = get_object_or_404(Comment, id=parent_id)
            comment.save()
            return redirect(self.object.get_absolute_url())
        else:
            context['comment_form'] = form  # Add the form with errors to the context
            return self.render_to_response(self.get_context_data(form=form))


def add_reply(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.comment = comment
            reply.save()
            return redirect('post_detail', pk=comment.id)
    else:
        form = ReplyForm()

    return render(request, 'post_detail.html', {'form': form})


def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = Post.objects.filter(active=True)
    new_comments = None
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        parent_id = request.POST.get('parent_id')
        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)
        else:
            parent_comment = None

        if comment_form.is_valid():
            new_comments = comment_form.save(commit=False)
            new_comments.post = post
            new_comments.user = request.user  # Ensure the comment is associated with the logged-in user
            new_comments.parent = parent_comment
            new_comments.save()
            return redirect('post_detail', slug=slug)
    else:
        comment_form = CommentForm()
    return render(request, template_name,
                  {'post': post, 'comments': comments, 'comment_form': comment_form, "new_comments": new_comments})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm  # Use the form that includes image and video
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
    form_class = PostForm  # Use the form that includes image and video
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'
    template_name = 'post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        assert isinstance(post.author, object)
        if self.request.user == post.author:
            return True
        return False

# API Views


# Create your views here.
