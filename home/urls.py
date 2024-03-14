from django.urls import path
from . import views

urlpatterns = [
    path('blogposts/', views.BlogViewSet.as_view(), name="blogpost-create-view"),
    path('blogposts/<int:pk>/', views.BlogRetrieveUpdateDestroy.as_view(), name="update"),
]
