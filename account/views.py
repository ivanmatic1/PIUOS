from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import RegisterSerializer


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
