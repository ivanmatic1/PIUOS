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
            return ''

class CategoryEnum(EnumMixin):
    SPORT = "Sport"
    LIFESTYLE = "Lifestyle"
    TECHNOLOGY = "Technology"


class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable = False, default = uuid.uuid4)
    created_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now_add = True)

    class Meta:
        abstract = True


class Blog(BaseModel):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "blogs")
    title = models.CharField(max_length=500)
    blog_text = models.TextField()
    category = models.CharField(max_length=20, choices=CategoryEnum.get_choices())
    
    def __str__(self) -> str:
        return self.title
    
class Comment(BaseModel):
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE, related_name = "comments" )
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "comments" )
    comment_text=models.CharField(max_length=5000)

class Like(BaseModel):
    blog = models.ForeignKey(Blog, on_delete = models.CASCADE, related_name = "likes" )
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "likes" )
    like_number=models.IntegerField()