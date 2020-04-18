from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.sessions.models import Session
from groups.models import Group,GroupMember
from django.contrib import messages
from django.contrib.auth import get_user_model
User=get_user_model()

from django import template
register=template.Library()

class Post(models.Model):
    user=models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)
    message=models.TextField()
    message_html=models.TextField(editable=False)
    def demo():
        session = Session.objects.first()
        uid = session.get_decoded().get('_auth_user_id')
        return {'members__id__icontains':uid}
    group=models.ForeignKey(Group,related_name='posts',limit_choices_to=demo,null=True,blank=True,on_delete=models.CASCADE)
    approved_post=models.BooleanField(default=False)

    def __str__(self):
        return str(self.message) if self.message else 'hell'

    def approve(self):
        self.approved_post=True
        self.save()

    def save(self,*args,**kwargs):
        # self.message_html=misaka.html(self.message)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        # messages.success(self.request,'Post Created Successfully!!')
        return reverse('posts:single',kwargs={'username':self.user.username,'pk':self.pk})

    class Meta:
        ordering=['-created_at']
        unique_together=['user','message']
