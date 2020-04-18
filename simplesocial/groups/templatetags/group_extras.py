from django import template
from groups.models import Group
from posts.models import Post
register = template.Library()

@register.filter(name='ccount')
def ccount(hell):
    return Post.objects.filter(approved_post='True',group=hell.id).count()