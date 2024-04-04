from django.urls import path
from home.views import BlogView, PublicBlogView, BlogDetailView, CommentListView, CommentDetailView, LikeBlogView, BlogLoggedDetailView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('blog/', BlogView.as_view()),  # Prikaz svih blogova i stvaranje novog bloga
    path('blog/<int:pk>/', BlogDetailView.as_view()),  # Detalji pojedinog bloga
    path('blog_logged/<int:pk>/', BlogLoggedDetailView.as_view()),  # Detalji pojedinog bloga
    path('', PublicBlogView.as_view()),  # Prikaz javnih blogova
    path('comments/', CommentListView.as_view()),  # Prikaz svih komentara i stvaranje novog komentara
    path('comments/<int:pk>/', CommentDetailView.as_view()),  # Detalji pojedinog komentara
    path('blog/<int:blog_id>/like/', LikeBlogView.as_view(), name='like-blog'),  # Dodavanje like/dislike na blog
]
urlpatterns = format_suffix_patterns(urlpatterns)  # Omogućava dodavanje formata na URL-ove