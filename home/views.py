from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import generics
from .models import Blog, Comment, Like
from rest_framework import status
from .serializer import BlogSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import Http404



class PublicBlogView(APIView):  # Definicija pogleda za javni pristup blogovima
    permission_classes = [AllowAny]
    authentication_classes = []
    def get(self, request):  # Definicija metode za HTTP GET zahtjev
        try:
            blogs = Blog.objects.all().order_by('?')  # Dohvaćanje svih blogova nasumičnim redoslijedom

            if request.GET.get('search'):  # Provjera postoji li parametar za pretragu
                search = request.GET.get('search')  # Dohvaćanje teksta za pretragu
                # Filtriranje blogova po naslovu, tekstu, kategoriji ili korisničkom imenu
                blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search) | Q(category__icontains=search) | Q(user__username__icontains=search))

            page_number = request.GET.get('page', 1)  # Dohvaćanje broja stranice, ako nije specificiran, postavlja se na 1
            paginator = Paginator(blogs, 10)  # Postavljanje broja blogova po stranici na 5

            serializer = BlogSerializer(paginator.page(page_number), many=True)  # Serijalizacija podataka u JSON format

            return Response({  # Generiranje odgovora
                'data': serializer.data,  # Podaci o blogovima
                'message': 'Blogs fetched successfully'  # Poruka o uspješnom dohvaćanju
            }, status.HTTP_200_OK)  # Status uspješnog odgovora

        except Exception as e:  # Hvatanje iznimki
            print(e)  # Ispisivanje iznimke u konzolu radi praćenja
            return Response({  # Generiranje odgovora u slučaju greške
                'data': {},  # Prazni podaci
                'message': 'Something went wrong or invalid page'  # Poruka o grešci
            }, status=status.HTTP_400_BAD_REQUEST)  # Status greške

class BlogView(APIView):  # Definicija pogleda za CRUD operacije s blogovima
    permission_classes = [IsAuthenticated]  # Postavljanje dozvola za pristup samo autenticiranim korisnicima
    authentication_classes = [JWTAuthentication]  # Postavljanje autentikacijskih klasa za JWT autentikaciju

    def get(self, request):  # Definicija metode za HTTP GET zahtjev
        try:
            # Dohvaćanje svih blogova
            blogs = Blog.objects.all()
            # Filtriranje blogova prema parametru za pretragu
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search) | Q(category__icontains=search) | Q(user__username__icontains=search))

            serializer = BlogSerializer(blogs, many=True)  # Serijalizacija podataka u JSON format

            return Response({  # Generiranje odgovora
                'data': serializer.data,  # Podaci o blogovima
                'message': 'Blogs fetched successfully'  # Poruka o uspješnom dohvaćanju
            }, status=status.HTTP_200_OK)  # Status uspješnog odgovora

        except Exception as e:  # Hvatanje iznimki
            print(e)  # Ispisivanje iznimke u konzolu radi praćenja
            return Response({  # Generiranje odgovora u slučaju greške
                'data': {},  # Prazni podaci
                'message': 'Something went wrong'  # Poruka o grešci
            }, status=status.HTTP_400_BAD_REQUEST)  # Status greške

    def post(self, request):  # Definicija metode za HTTP POST zahtjev
        try:
            data = request.data  # Dohvaćanje podataka iz zahtjeva
            data['user'] = request.user.id  # Postavljanje korisnika koji je stvorio blog na trenutno prijavljenog korisnika
            serializer = BlogSerializer(data=data)  # Serijalizacija podataka u JSON format

            serializer.is_valid(raise_exception=True)  # Provjera valjanosti podataka

            serializer.save()  # Spremanje novog bloga

            return Response({  # Generiranje odgovora
                'data': serializer.data,  # Podaci o stvorenom blogu
                'message': 'Blog created successfully'  # Poruka o uspješnom stvaranju
            }, status=status.HTTP_201_CREATED)  # Status uspješnog stvaranja

        except Exception as e:  # Hvatanje iznimki
            print(e)  # Ispisivanje iznimke u konzolu radi praćenja
            return Response({  # Generiranje odgovora u slučaju greške
                'data': {},  # Prazni podaci
                'message': 'Something went wrong'  # Poruka o grešci
            }, status=status.HTTP_400_BAD_REQUEST)  # Status greške

    def patch(self, request):  # Definicija metode za HTTP PATCH zahtjev
        try:
            data = request.data  # Dohvaćanje podataka iz zahtjeva

            blog = Blog.objects.filter(id=data.get('id'))  # Dohvaćanje bloga prema ID-u iz podataka

            if not blog.exists():  # Provjera postoji li blog s tim ID-om
                return Response({  # Generiranje odgovora u slučaju nevažećeg ID-a
                    'data': {},  # Prazni podaci
                    'message': 'Invalid blog ID'  # Poruka o nevažećem ID-u
                }, status=status.HTTP_400_BAD_REQUEST)  # Status greške

            if request.user != blog[0].user:  # Provjera je li korisnik koji šalje zahtjev autor bloga
                return Response({  # Generiranje odgovora u slučaju neautoriziranog pristupa
                    'data': {},  # Prazni podaci
                    'message': 'You are not authorized to do this'  # Poruka o neautoriziranom pristupu
                }, status=status.HTTP_400_BAD_REQUEST)  # Status greške

            serializer = BlogSerializer(blog[0], data, partial=True)  # Serijalizacija podataka u JSON format

            if not serializer.is_valid():  # Provjera valjanosti podataka
                return Response({  # Generiranje odgovora u slučaju nevaljanosti podataka
                    'data': serializer.errors,  # Greške u podacima
                    'message': 'Something went wrong'  # Poruka o grešci
                }, status=status.HTTP_400_BAD_REQUEST)  # Status greške

            serializer.save()  # Spremanje ažuriranih podataka o blogu

            return Response({  # Generiranje odgovora
                'data': serializer.data,  # Ažurirani podaci o blogu
                'message': 'Blog updated successfully'  # Poruka o uspješnom ažuriranju
            }, status.HTTP_201_CREATED)  # Status uspješnog ažuriranja

        except Exception as e:  # Hvatanje iznimki
            print(e)  # Ispisivanje iznimke u konzolu radi praćenja
            return Response({  # Generiranje odgovora u slučaju greške
                'data': {},  # Prazni podaci
                'message': 'Something went wrong'  # Poruka o grešci
            }, status=status.HTTP_400_BAD_REQUEST)  # Status greške
        
    def delete(self, request):  # Definicija metode za HTTP DELETE zahtjev
        try:
            data = request.data  # Dohvaćanje podataka iz zahtjeva

            blog = Blog.objects.filter(id=data.get('id'))  # Dohvaćanje bloga prema ID-u iz podataka

            if not blog.exists():  # Provjera postoji li blog s tim ID-om
                return Response({  # Generiranje odgovora u slučaju nevažećeg ID-a
                    'data': {},  # Prazni podaci
                    'message': 'Invalid blog ID'  # Poruka o nevažećem ID-u
                }, status=status.HTTP_400_BAD_REQUEST)  # Status greške

            if request.user != blog[0].user:  # Provjera je li korisnik koji šalje zahtjev autor bloga
                return Response({  # Generiranje odgovora u slučaju neautoriziranog pristupa
                    'data': {},  # Prazni podaci
                    'message': 'You are not authorized to do this'  # Poruka o neautoriziranom pristupu
                }, status=status.HTTP_400_BAD_REQUEST)  # Status greške

            blog[0].delete()  # Brisanje odabranog bloga

            return Response({  # Generiranje odgovora
                'data': {},  # Prazni podaci
                'message': 'Blog deleted successfully'  # Poruka o uspješnom brisanju
            }, status.HTTP_201_CREATED)  # Status uspješnog brisanja

        except Exception as e:  # Hvatanje iznimki
            print(e)  # Ispisivanje iznimke u konzolu radi praćenja
            return Response({  # Generiranje odgovora u slučaju greške
                'data': {},  # Prazni podaci
                'message': 'Something went wrong'  # Poruka o grešci
            }, status=status.HTTP_400_BAD_REQUEST)  # Status greške
            
class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = []
    authentication_classes = []

    def get_object(self):
        try:
            instance = super().get_object()
            return instance
        except Blog.DoesNotExist:
            raise Http404

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            comments = instance.comments.all()
            comment_serializer = CommentSerializer(comments, many=True)

            return Response({
                'blog': serializer.data,
                'comments': comment_serializer.data,
                'user_like_choice': serializer.data['user_like_choice']
            })

        except Http404: 
            return Response({'message': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

"""Ovaj dio se odnosi na komentiranje"""
class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()  # Postavljanje queryseta na sve instance modela Comment
    serializer_class = CommentSerializer  # Postavljanje serializer klase na CommentSerializer
    permission_classes = [IsAuthenticated]  # Definiranje prava pristupa
    authentication_classes = [JWTAuthentication]  # Definiranje metoda autentifikacije

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Postavljanje trenutnog korisnika kao autora komentara

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()  # Postavljanje queryseta na sve instance modela Comment
    serializer_class = CommentSerializer  # Postavljanje serializer klase na CommentSerializer
    permission_classes = [IsAuthenticated]  # Definiranje prava pristupa
    authentication_classes = [JWTAuthentication]  # Definiranje metoda autentifikacije

class LikeBlogView(APIView):
    permission_classes = [IsAuthenticated]  # Definiranje prava pristupa
    authentication_classes = [JWTAuthentication]  # Definiranje metoda autentifikacije
    def post(self, request, blog_id):
        try:
            blog = Blog.objects.get(pk=blog_id)  # Dohvaćanje bloga na koji se dodaje like/dislike
            like_choice = request.data.get('like_choice')  # Dohvaćanje izbora korisnika ('like' ili 'dislike')

            if like_choice not in ['like', 'dislike']:  # Provjera valjanosti izbora
                return Response({'message': 'Invalid like choice'}, status=status.HTTP_400_BAD_REQUEST)

            user = request.user  # Dohvaćanje trenutnog korisnika

            if blog.user_liked_blog(user):  # Provjera je li korisnik već lajkao blog
                current_like_choice = blog.get_user_like_choice(user)
                if current_like_choice == like_choice:  # Ako korisnik pokušava ponovno lajkati ono što već lajka
                    blog.likes.filter(user=user).delete()  # Uklanja like/dislike
                else:  # Ako korisnik mijenja like u dislike ili obrnuto
                    blog.likes.filter(user=user).update(like_choice=like_choice)  # Ažurira like/dislike
            else:  # Ako korisnik prvi put lajka ili dislajka blog
                Like.objects.create(user=user, blog=blog, like_choice=like_choice)  # Stvara novi like/dislike

            return Response({'message': 'Like/Dislike added successfully'}, status=status.HTTP_201_CREATED)

        except Blog.DoesNotExist:  # Ako blog ne postoji
            return Response({'message': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:  # Ako se dogodi bilo kakva druga greška
            print(e)
            return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)