from django.urls import path
from . import views
from .views import PostListView,PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, latest_posts

urlpatterns = [
    path('', views.home, name="diary-home"),
    path('about/', views.about, name="blog-about"),
    path('latest-posts/', latest_posts, name='latest_posts'),
    path('comment/<int:comment_id>/reply/', views.add_reply, name='add_reply'),
    path('post/<int:pk>/', PostDetailView.as_view(), name="blog-detail"),
    path('', PostListView.as_view(), name="blog-home"),
    path('post-new/', PostCreateView.as_view(), name="blog-new"),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name="blog-update"),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="blog-delete")
]
