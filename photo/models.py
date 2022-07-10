from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Photo(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_photos')
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
        return reverse('photo:photo_detail', args=[str(self.id)])

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_photoss')
    photo=models.ForeignKey(Photo, on_delete=models.CASCADE)
    content=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content