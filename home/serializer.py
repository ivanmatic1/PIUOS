from rest_framework import serializers
from .models import Blog, Comment  # Uvoz modela Blog i Comment iz istog direktorija
from django.contrib.auth.models import User

# Serializer za Blog modele
class BlogSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()  # Serializer polje koje će vratiti korisničko ime
    likes = serializers.SerializerMethodField()  # Serializer polje koje će vratiti informacije o lajkovima

    class Meta:
        model = Blog  # Postavljanje modela na Blog
        fields = ['id', 'title', 'blog_text', 'user','category', 'comments', 'user_name', 'likes', 'created_at']  # Polja koja će biti uključena u serijalizaciju

    def get_user_name(self, obj):
        return obj.user.username  # Metoda koja vraća korisničko ime autora bloga

    def get_likes(self, obj):
        return {
            'like_number': obj.likes.filter(like_choice='like').count(),  # Broj lajkova na blogu
            'dislike_number': obj.likes.filter(like_choice='dislike').count(),  # Broj dislajkova na blogu
            'user_like_choice': obj.get_user_like_choice(self.context['request'].user) if self.context.get('request') else None  # Izbor korisnika (lajk, dislajk, ili None ako korisnik nije lajkao)
        }

# Serializer za User modele
class UserSerializer(serializers.ModelSerializer):
    blogs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Serializer polje za prikaz primarnih ključeva povezanih blogova korisnika
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Serializer polje za prikaz primarnih ključeva povezanih komentara korisnika

    class Meta:
        model = User  # Postavljanje modela na User
        fields = ['id', 'username', 'blogs', 'comments']  # Polja koja će biti uključena u serijalizaciju

# Serializer za Comment modele
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Serializer polje koje će vratiti korisničko ime autora komentara

    class Meta:
        model = Comment  # Postavljanje modela na Comment
        fields = ['id', 'comment_text', 'user', 'blog']  # Polja koja će biti uključena u serijalizaciju
