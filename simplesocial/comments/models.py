from django.db import models
from django.utils import timezone
from django.urls import reverse
from posts.models import Post
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your models here.

from django import template
register=template.Library()

class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    author=models.ForeignKey(User,related_name='authors',on_delete=models.CASCADE)
    text=models.TextField(validators=[MinLengthValidator(1,'No blank comments allowed!')])
    created_date=models.DateTimeField(default=timezone.now)
    approved_comment=models.BooleanField(default=False)

    def approve(self):
        self.approved_comment=True
        self.save()

    def get_absolute_url(self):
        return reverse('/')

    def __str__(self):
        return self.text