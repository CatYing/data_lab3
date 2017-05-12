# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.apps import apps
from django.core import serializers
from models import *


# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


class AnyView(TemplateView):
    template_name = 'query_any.html'

    def get_context_data(self, **kwargs):
        context = super(AnyView, self).get_context_data(**kwargs)
        app_config = apps.get_app_config('lab3')
        models_list = app_config.get_models()
        models_name_list = [model.__name__ for model in models_list]
        context['models_list'] = models_name_list
        return context


class LevelCreateView(CreateView):
    template_name = 'level-create.html'
    model = Level
    fields = ['name']
    success_url = reverse_lazy("level-create")

    def get_context_data(self, **kwargs):
        context = super(LevelCreateView, self).get_context_data(**kwargs)
        context['level_list'] = Level.objects.all().order_by('pk')
        return context


class LevelUpdateView(TemplateView):
    template_name = 'level-update.html'

    def get_context_data(self, **kwargs):
        context = super(LevelUpdateView, self).get_context_data(**kwargs)
        context['level_list'] = Level.objects.all().order_by('pk')
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            return super(LevelUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            level_pk = int(request.POST.get("pk"))
            level = Level.objects.get(pk=level_pk)
            level_name = request.POST.get("name")
            if Level.objects.filter(name=level_name).count() >= 1:
                return HttpResponse(json.dumps({'result': 0, 'message': "已有相同名字的学历级别"}), content_type='application/json')
            else:
                level.name = level_name
                level.save()
                return HttpResponse(json.dumps({'result': 1}), content_type='application/json')


def delete_level(request):
    if request.GET.get('id'):
        level_id = int(request.GET.get('id'))
        level = Level.objects.get(pk=level_id)
        level.delete()
    return render(request, 'level-delete.html', context={'level_list': Level.objects.all().order_by('pk')})


class UserListView(ListView):
    template_name = 'user-list.html'
    model = User
    context_object_name = 'user_list'

    def get_queryset(self):
        return User.objects.order_by('-birthday')


class UserFriendsListView(TemplateView):
    template_name = 'friend-list.html'

    def get_context_data(self, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        context = super(UserFriendsListView, self).get_context_data(**kwargs)
        context['user'] = user
        group_list = FriendGroup.objects.filter(user=user)
        context['group_list'] = group_list
        friend_list = []
        for group in group_list:
            for friend in group.friendsrelation_set.all():
                friend_list.append(friend.friend.name)
        context['friend_list'] = friend_list
        return context


class UserEducationMixView(TemplateView):
    template_name = 'mix-edu.html'

    def get_context_data(self, **kwargs):
        context = super(UserEducationMixView, self).get_context_data(**kwargs)
        user_list = []
        for user in User.objects.all():
            if user.education_set.all().count() == 1:
                if user.education_set.all()[0].level.name == u'本科':
                    user_list.append(user.name)
        context['user_list'] = user_list
        return context


class UserEducationGroupView(TemplateView):
    template_name = 'group-edu.html'

    def get_context_data(self, **kwargs):
        context = super(UserEducationGroupView, self).get_context_data(**kwargs)
        user_list = User.objects.filter(education__in=Education.objects.filter(level__name=u'硕士'))
        context['user_list'] = user_list
        return context


def error(request, message):
    return render(request, "error.html", context={'message': message})


def api_query_any(request):
    app_config = apps.get_app_config('lab3')
    print request.POST.get("model")
    model = app_config.get_model(request.POST.get("model"))
    data = serializers.serialize('json', model.objects.all().order_by('pk'))
    return HttpResponse(data, content_type='application/json')
