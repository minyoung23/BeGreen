from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Board(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_photo', null=True)
    photo=models.ImageField(upload_to='photos/%Y/%m/%d', null=True, blank=True)
    title=models.CharField(max_length=50, null=True, blank=True)
    text=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-updated']

    def __str__(self):
        return self.author.username

    def get_absolute_url(self):
        return reverse('board:board_detail', args=[str(self.id)])
