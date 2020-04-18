from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse,reverse_lazy
from django.contrib import messages
from django.views import generic
from groups.models import Group,GroupMember
from django.http import Http404,HttpResponseRedirect
from . import models
from django.db import IntegrityError
# Create your views here.

class DeleteGroupMember(LoginRequiredMixin,generic.DeleteView):
    model=GroupMember
    login_url='/login/'
    # success_url=reverse_lazy('groups:all')

    def get_object(self,*args,**kwargs):
        obj=get_object_or_404(GroupMember,user=self.kwargs['user'],group=self.kwargs['group'])
        gay=models.Group.objects.filter(id=self.kwargs['group']).values('created_by')[0]
        if(gay['created_by']==self.request.user.id and not str(gay['created_by'])==str(self.kwargs['user'])):
            return obj
        raise Http404
    
    def get_success_url(self,*args,**kwargs):
        gay=models.Group.objects.filter(id=self.kwargs['group']).values('slug')[0]
        return reverse('groups:single',kwargs={'slug':gay['slug']})

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields=('name','description')
    model=Group

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self,*args,**kwargs):
        messages.success(self.request,'You have successfully created this group!!!')
        return reverse('groups:join',kwargs={'slug':self.object.slug})

class UpdateGroup(LoginRequiredMixin,generic.UpdateView):
    fields=('name','description')
    model=Group

    def get_object(self,*args,**kwargs):
        obj=super().get_object()
        # print(self.request.POST.get('name'))
        if(self.request=='POST'):
            gay=models.Group.objects.filter(slug=self.request.POST.get('name')).values('created_by')[0]
            if(self.request.user.id==gay['created_by']):
                return obj
        else:
            gay=models.Group.objects.filter(slug=self.kwargs['slug']).values('created_by')[0]
            if(self.request.user.id==gay['created_by']):
                return obj
        # qs=queryset.filter(user_id=self.request.user.id) | queryset.filter(user_id=gay['group__created_by'])
        raise Http404

    def get_success_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.request.POST.get('name')})

class SingleGroup(generic.DetailView):
    model=Group

class ListGroup(generic.ListView):
    model=Group

class DeleteGroup(LoginRequiredMixin,generic.DeleteView):
    model=Group
    login_url='/login/'
    success_url=reverse_lazy('groups:all')

    def get_object(self,*args,**kwargs):
        obj=super().get_object()
        gay=models.Group.objects.filter(slug=self.kwargs['slug']).values('created_by')[0]
        if(self.request.user.id==gay['created_by']):
            return obj
        # qs=queryset.filter(user_id=self.request.user.id) | queryset.filter(user_id=gay['group__created_by'])
        raise Http404

class JoinGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        group=get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user,group=group)

        except IntegrityError:
            messages.warning(self.request,'You are already a member!')
        else:
            messages.success(self.request,'You have successfully joined this group!!!')

        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        try:
            membership=models.GroupMember.objects.filter(user=self.request.user,group__slug=self.kwargs.get('slug')).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,'You are not in the group')
        else:
            membership.delete()
            messages.success(self.request,'Successfully left the group!!!')
        return super().get(request,*args,**kwargs)
