from django.db import models
from django.contrib.auth.models import User
import uuid
from enum import Enum

class EnumMixin(Enum):

    @classmethod
    def get_choices(cls):
        return ((pt.name, pt.value) for pt in cls)

    @classmethod
    def get_value(cls, name):
        try:
            return cls[name].value
        except KeyError:
            raise ValueError(f"No such value for {name}")

# Definicija kategorija pomoću EnumMixin
class CategoryEnum(EnumMixin):
    SPORT = "Sport"
    LIFESTYLE = "Lifestyle"
    TECHNOLOGY = "Technology"

# Bazni model sa zajedničkim poljima
class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True  # Postavljanje modela kao apstraktnog

# Model Bloga s vezama prema korisniku, kategoriji, komentarima i lajkovima
class Blog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=500)
    blog_text = models.TextField()
    category = models.CharField(max_length=20, choices=CategoryEnum.get_choices())
    
    def __str__(self) -> str:
        return self.title
    
    # Metode za provjeru lajkova korisnika na blogu
    def user_liked_blog(self, user):
        return self.likes.filter(user=user).exists()

    def get_user_like_choice(self, user):
            if user.is_authenticated:  # Provjera je li korisnik autenticiran
                like = self.likes.filter(user=user).first()  # Dohvaćanje lajka/dislajka ako postoji
                if like:
                    return like.like_choice  # Vraćanje odabira lajka/dislajka
            return None  # Vraćanje None ako korisnik nije autenticiran ili ako nije lajkao/dislajkao
    
# Model komentara s vezama prema korisniku i blogu
class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField(blank=False)
    user = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    blog = models.ForeignKey('Blog', related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']  # Postavljanje redoslijeda komentara

# Model lajkova s vezama prema korisniku i blogu
class Like(models.Model):
    LIKE_CHOICES = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    like_choice = models.CharField(max_length=7, choices=LIKE_CHOICES)

    class Meta:
        unique_together = ('user', 'blog')  # Postavljanje jedinstvenog para korisnika i bloga
