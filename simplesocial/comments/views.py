from django.shortcuts import render,get_object_or_404,redirect,redirect,HttpResponseRedirect
from django.utils import timezone
from posts.models import Post
from comments.models import Comment
from comments.forms import CommentForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.http import Http404
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if (request.method=='POST'):
        if(request.user in post.group.members.all()):
            text=request.POST.get('com')
            if(len(text)==0):
                raise ValidationError("No Blank Comments are allowed!!")
            if(request.user==post.user):
                Comment.objects.create(text=text,post=post,author=request.user,approved_comment=True)
            else:
                Comment.objects.create(text=text,post=post,author=request.user)
            messages.success(request,'Comment posted successfully!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            # return redirect('groups:single',slug=post.group.slug)
        raise Http404

@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    if(request.user==comment.post.user):
        comment.approved_comment=True
        comment.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # return redirect('groups:single',slug=comment.post.group.slug)
    raise Http404

@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    if(request.user==comment.author or request.user==comment.post.user):
        post_pk=comment.post.pk
        comment.delete()
        messages.success(request,'Comment deleted successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # return redirect('groups:single',slug=comment.post.group.slug)
    raise Http404
