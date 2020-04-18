from django import template
from groups.models import Group
from posts.models import Post
register = template.Library()

@register.filter(name='cccount')
def cccount(hell):
    return Post.objects.filter(approved_post='True',user=hell.id).count()

@register.filter(name='scount')
def scount(hell):
    return Post.objects.filter(approved_post='False',user=hell.id).count()