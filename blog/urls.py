from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name='home'),
    path('search/', views.search_results, name='search_results'),

    path('posts/', views.PostListView.as_view(), name='all_posts'),
    path('posts/new/', views.PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/', views.CommentCreateView.as_view(), name='post_comment'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    path('comments/<int:pk>/edit', views.CommentEditView.as_view(), name='edit_comment')
]
