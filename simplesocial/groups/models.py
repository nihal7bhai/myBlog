from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# from django.contrib.sessions.models import Session
from django.conf import settings
# Create your models here.

# import misaka
from django.contrib.auth import get_user_model
User=get_user_model()

from django import template
register=template.Library()

class Group(models.Model):
    name=models.CharField(max_length=255,unique=True)
    slug=models.SlugField(allow_unicode=True,unique=True)
    description=models.TextField(blank=True,default="")
    description_html=models.TextField(editable=False,default="",blank=True)
    members=models.ManyToManyField(User,through='GroupMember')
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='created_by',default='')
    def __str__(self):
        return self.name if self.name else ''

    def save(self,*args,**kwargs):
        self.slug=slugify(self.name)
        # self.created_by=User
        # print("add: ",self.created_by)
        # self.description_html=misaka.html(self.description)
        super().save(*args,**kwargs)

    class Meta:
        ordering=['name']

class GroupMember(models.Model):
    group=models.ForeignKey(Group,related_name='memberships',on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name='user_groups',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username if self.user.username else ''

    class Meta:
        unique_together=('group','user')