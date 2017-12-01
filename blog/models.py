from django.db import models

# Create your models here.


class Post(models.Model):
    title= models.CharField(max_length=64,default='Title')
    profile = models.TextField(null=True)
    content = models.TextField(null=True)
    pub_time = models.DateTimeField(null=True)