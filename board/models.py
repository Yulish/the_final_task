from django.db import models
from django.contrib.auth.models import User, Group
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.db import models
import random
import string


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Poster(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    head = models.CharField(max_length=255)
    text = RichTextUploadingField()
    categories = models.ManyToManyField(Category)
    poster_origin = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.head} (от {self.user.username})"

    def get_absolute_url(self):
        return reverse('poster_detail', args=[str(self.id)])


class Response(models.Model):
    poster = models.ForeignKey(Poster, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresser')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'recipient')
    status = models.BooleanField(default=False)
    response = models.TextField(max_length=10000, blank=True)
    response_origin = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f'{self.response}'

    def get_detail_url(self):
        return reverse('response_detail', args=[str(self.id)])


class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, blank=True)

    def generate_code(self):
        self.code = ''.join(random.choices(string.digits, k=6))
        self.save()









