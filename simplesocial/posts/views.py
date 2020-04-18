from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.http import Http404
from braces.views import SelectRelatedMixin
# Create your views here.
from groups import models as gmdel
from . import models
from . import forms

from django.contrib.auth import get_user_model
User=get_user_model()

class PostList(SelectRelatedMixin,generic.ListView):
    model=models.Post
    select_related=('user','group')

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['gg']=gmdel.Group.objects.all()
        return context

class UserPosts(generic.ListView):
    model=models.Post
    template_name='posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user=User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['post_user']=self.post_user
        return context

class PostDetail(SelectRelatedMixin,generic.DetailView):
    model=models.Post
    select_related=('user','group')

    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    fields=('message','group')
    model=models.Post
    # template_name='posts/post_form.html'

    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user 
        try:
            gay=models.Group.objects.filter(pk=self.object.group.id).values('created_by')[0]
            if(self.object.group and gay['created_by']==self.request.user.id):
                self.object.approved_post=True
        except:
            self.object.approved_post=True
        self.object.save()
        return super().form_valid(form)

class UpdatePost(LoginRequiredMixin,SelectRelatedMixin,generic.UpdateView):
    fields=('message',)
    select_related=('user','group')
    model=models.Post
    # success_url=reverse_lazy('posts:for_user',username=self.request.user.username)
    # template_name='posts/post_form.html'

    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def get_object(self):
        obj=super().get_object()
        obj.approved_post = False
        return obj

    def get_success_url(self):
        messages.success(self.request,'Post Updated Successfully!!')
        return reverse_lazy('posts:single', kwargs={'pk':self.object.pk,'username': self.object.user.username})

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model=models.Post
    select_related=('user','group')
    # success_url=reverse_lazy('posts:all')

    def get_object(self,*args,**kwargs):
        obj=super().get_object()
        gay=models.Post.objects.filter(pk=self.kwargs['pk']).values('group__created_by','user__id')[0]
        # gay1=models.Post.objects.filter(pk=self.kwargs['pk']).values('user__id')[0]
        # print(gay['group__created_by'])
        if(str(self.request.user.id)==str(gay['group__created_by']) or str(self.request.user.id)==str(gay['user__id'])):
            return obj
        # qs=queryset.filter(user_id=self.request.user.id) | queryset.filter(user_id=gay['group__created_by'])
        return Http404

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted Successfully!!')
        return super().delete(*args,**kwargs)

    def get_success_url(self):
        # return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        return reverse_lazy('posts:for_user', kwargs={'username': self.object.user.username})

def post_approve(request,pk):
    post=get_object_or_404(models.Post,pk=pk)
    post.approve()
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('groups:single',slug=post.group.slug)