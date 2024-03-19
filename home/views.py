from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import generics
from .models import Blog
from rest_framework import status
from .serializer import BlogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from django.core.paginator import Paginator




class PublicBlogView(APIView): #view za korisnike koji nisu registrirani
    def get(self, request):
        try:

            blogs=Blog.objects.all().order_by('?')

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs=blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search) | Q(category__icontains=search)) 

            page_number = request.GET.get('page', 1)
            paginator = Paginator(blogs, 5)
            
            serializer = BlogSerializer(paginator.page(page_number), many=True)

            return Response({
                'data' : serializer.data,
                'message' : 'Blogs fetched successfully'

                }, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                'data' : {},
                'message' : 'Something went wrong or invalid page'

            }, status = status.HTTP_400_BAD_REQUEST)






class BlogView(APIView):
     
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get (self, request):
        try:
            blogs=Blog.objects.filter(user=request.user)

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs=blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search) | Q(category__icontains=search)) 

            serializer = BlogSerializer(blogs, many=True)

            return Response({
                'data' : serializer.data,
                'message' : 'Blogs fetched successfully'

                }, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                'data' : {},
                'message' : 'Something went wrong'

            }, status = status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            data = request.data
            data['user']=request.user.id
            serializer = BlogSerializer(data=data)

            print('######')
            print(request.user)
            print(request.user.id)
            print('######')

            if not serializer.is_valid():
                return Response({
                    'data' : serializer.errors,
                    'message' : 'Something went wrong'

                }, status = status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                'data' : serializer.data,
                'message' : 'Blog created successfully'

                }, status.HTTP_201_CREATED)
        
        

        
        except Exception as e:
            print(e)
            return Response({
                'data' : serializer.errors,
                'message' : 'Something went wrong'

            }, status = status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            data = request.data

            blog = Blog.objects.filter(uid=data.get('uid'))
           
            if not blog.exists():
                return Response({
                    'data' : {},
                    'message' : 'Invalid blog ID'

                }, status = status.HTTP_400_BAD_REQUEST)
            
            if request.user != blog[0].user: #provjerava da li je user koji salje request autor bloga
                return Response({
                    'data' : {},
                    'message' : 'You are not authorized to do this'

            }, status = status.HTTP_400_BAD_REQUEST)

            
            
            serializer  = BlogSerializer(blog[0], data, partial = True)
            if not serializer.is_valid():
                return Response({
                    'data' : serializer.errors,
                    'message' : 'Something went wrong'

                }, status = status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data' : serializer.data,
                'message' : 'Blog updated successfully'

                }, status.HTTP_201_CREATED)
        

        except Exception as e:
            print(e)
            return Response({
                'data' : {},
                'message' : 'Something went wrong'

            }, status = status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        try:
            data = request.data

            blog = Blog.objects.filter(uid=data.get('uid'))
           
            if not blog.exists():
                return Response({
                    'data' : {},
                    'message' : 'Invalid blog ID'

                }, status = status.HTTP_400_BAD_REQUEST)
            
            if request.user != blog[0].user:
                return Response({
                    'data' : {},
                    'message' : 'You are not authorized to do this'

            }, status = status.HTTP_400_BAD_REQUEST)
        
            blog[0].delete()

            return Response({
                'data' : {},
                'message' : 'Blog deleted successfully'

            }, status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                'data' : {},
                'message' : 'Something went wrong'

            }, status = status.HTTP_400_BAD_REQUEST)        