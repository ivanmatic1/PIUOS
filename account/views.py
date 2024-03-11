from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import RegisterSerializer


class RegisterView(APIView):
    
    def post(self, request):
        data = request.data
        serializer =  RegisterSerializer(data=data)
        try:
            
            

            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message': 'Something went wrong'
                }, status = status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(
            {
                'data':{},
                'message': 'Your account is created succesfully!',
            }, status = status.HTTP_201_CREATED
            )
            

        except Exception as e:
               if not serializer.is_valid():
                return Response(
                {
                    'data':{},
                    'message': 'Something went wrong',
                }, status = status.HTTP_400_BAD_REQUEST
                )
