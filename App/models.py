from django.db import models
from django.contrib.auth.models import User,AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    bio=models.TextField()
    location=models.CharField(max_length=255)

class Q(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    content=models.TextField()
    tags=models.TextField(default='')
    added_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class A(models.Model):
    q=models.ForeignKey(Q,on_delete=models.CASCADE,related_name='answer_set')
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    a=models.TextField()
    added_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.a


class Comments(models.Model):
    answer=models.ForeignKey(A,on_delete=models.CASCADE,related_name='content_set')
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    content=models.TextField(default='')
    added_on=models.DateTimeField(auto_now_add=True)

    

    

class Upvotes(models.Model):
    answer=models.ForeignKey(A,on_delete=models.CASCADE,related_name='upvote_set')
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    
class Downvotes(models.Model):
    answer=models.ForeignKey(A,on_delete=models.CASCADE,related_name='downvote_set')
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    

