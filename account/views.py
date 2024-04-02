from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from .serializer import RegisterSerializer, LoginSerializer, UserProfileSerializer, UserListSerializer
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from django.core.paginator import Paginator
class RegisterView(APIView): #view za registraciju korisnika
    
    def post(self, request): #funkcija za postanje podataka za registraciju
        data = request.data
        serializer =  RegisterSerializer(data=data)
        try:

            if not serializer.is_valid(): #ako serializer nije validan
                return Response({
                    'data':serializer.errors,
                    'message': 'Something went wrong'
                }, status = status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response( #else account se kreira
            {
                'data':{},
                'message': 'Your account is created succesfully!',
            }, status = status.HTTP_201_CREATED
            )
            

        except Exception as e:  #raisa exception ako nešto nije u redu
               if not serializer.is_valid():
                return Response(
                {
                    'data':{},
                    'message': 'Something went wrong',
                }, status = status.HTTP_400_BAD_REQUEST
                )


class LoginView(APIView):
    def post (self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)

            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message': 'Something went wrong'
                }, status = status.HTTP_400_BAD_REQUEST)
            
            response = serializer.get_jwt_token(serializer.data)

            return Response(response,status = status.HTTP_200_OK)
        
        except Exception as e:  #raisa exception ako nešto nije u redu
            print(e)
            return Response(
                {
                    'data':{},
                    'message': 'Something went wrong',
                }, status = status.HTTP_400_BAD_REQUEST
                )
        
class UserProfileDetailView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UserListView(APIView):
    
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def get (self, request):
        try:
            users=User.objects.all()

            if request.GET.get('search'):
                search = request.GET.get('search')
                users=users.filter(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(username__icontains=search)) 

            

            if not users.exists():  # Provjerite je li queryset prazan
                    return Response({
                        'data': [],
                        'message': 'No users found with the provided search criteria'
                    }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserListSerializer(users, many=True)

            return Response({
                'data' : serializer.data,
                'message' : 'Users fetched successfully'

                }, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                'data' : {},
                'message' : 'Something went wrong'

            }, status = status.HTTP_400_BAD_REQUEST)
class UserDetailView(APIView):
    def get(self, request):
        try:
            username = request.GET.get('username')
            first_name = request.GET.get('first_name')
            last_name = request.GET.get('last_name')

            users = User.objects.all().order_by('?')

            if username:
                users = users.filter(username__icontains=username)
            if first_name:
                users = users.filter(first_name__icontains=first_name)
            if last_name:
                users = users.filter(last_name__icontains=last_name)

            if not users.exists():
                return Response({
                    'data': {},
                    'message': 'User not found'
                }, status=status.HTTP_404_NOT_FOUND)

            page_number = request.GET.get('page', 1)
            paginator = Paginator(users, 5)

            serializer = UserProfileSerializer(paginator.page(page_number), many=True)

            return Response({
                'data': serializer.data,
                'message': 'Users fetched successfully'
            }, status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong or invalid page'
            }, status=status.HTTP_400_BAD_REQUEST)
