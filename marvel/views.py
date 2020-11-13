import json

import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from marvel.forms import UserLoginForm
from marvel.models import Comics
from marvel_comics.settings import API_URL, MARVEL_PUBLIC_KEY, MARVEL_SECRET_KEY
from marvel.handlers import get_hash_string, ts_generator, prepare_comics_data

TS = ts_generator()
hash_string = get_hash_string(TS, MARVEL_SECRET_KEY, MARVEL_PUBLIC_KEY)


def home_page(request):
    return redirect('marvel:comics_api_list')


def get_data_from_api(_hash_string, url=API_URL, **kwargs):
    """делаем запрос к api marvel"""
    params = {
        'apikey': MARVEL_PUBLIC_KEY,
        'ts': TS,
        'hash': _hash_string,
    }
    params.update(kwargs)

    api_data = requests.get(url=url, params=params)
    api_data_text = json.loads(api_data.text)
    result = api_data_text['data']['results']
    return result


class ComicsListAPIView(generics.ListAPIView):
    """Вью для всех комиксов"""
    renderer_classes = (TemplateHTMLRenderer,)
    context = dict()

    def get(self, request):
        self.context['comics'] = []
        if request.query_params:
            comics_data = get_data_from_api(_hash_string=hash_string, title=request.query_params['title'])
            for comics in comics_data:
                self.context['comics'].append(comics)
        return Response(self.context, template_name='comics_list_api.html')


class ComicsDetailView(generics.RetrieveAPIView):
    """Вью для комикса"""
    renderer_classes = (TemplateHTMLRenderer,)
    context = dict()

    def get(self, request, comic_id):
        comic = get_data_from_api(_hash_string=hash_string, id=comic_id)
        self.context.update({'comic': comic[0]})
        return Response(self.context, template_name='comics_detail_api.html')


class UserLoginView(LoginView):
    """Вью для логина пользователя"""
    form_class = UserLoginForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse('marvel:comics_api_list')


class UserLogOutView(LogoutView):
    pass


class ComicsCreateView(LoginRequiredMixin, CreateView):
    """Вью создания Комикса в базе"""
    model = Comics

    def post(self, request, comic_id, *args, **kwargs):

        comic = get_data_from_api(_hash_string=hash_string, id=comic_id)
        profile_comicses = Comics.objects.filter(profile=request.user.profile.id)

        if not profile_comicses.filter(comics_id=comic_id).exists():
            comics_data, stories, characters, creators, images = prepare_comics_data(comic[0])

            saved_comics = Comics.objects.create(**comics_data)
            current_user = request.user.profile
            current_user.comics.add(saved_comics)
            saved_comics.stories.add(*stories)
            saved_comics.characters.add(*characters)
            saved_comics.creators.add(*creators)
            saved_comics.images.add(*images)

        return redirect('marvel:comics_api_detail', comic_id)


class ComicsUpdateView(LoginRequiredMixin, UpdateView):
    """Вью апдейта комикса"""
    model = Comics
    fields = '__all__'
    template_name = 'comics_form.html'


class ComicsDeleteView(LoginRequiredMixin, DeleteView):
    """Вью удаления комикса"""
    model = Comics
    template_name = 'comics_confirm_delete.html'

    def get_success_url(self):
        return reverse('marvel:master_list')


class ProfileComicsList(LoginRequiredMixin, ListView):
    """Вью просмотра комиксов пользователя"""
    model = Comics
    template_name = 'profile_comics_list.html'

    def get_queryset(self):
        queryset = Comics.objects.filter(profile__user_id=self.request.user.id)
        return queryset


class ProfileComicsDetail(LoginRequiredMixin, DetailView):
    """Вью детального просмотра комикса у пользователя"""
    model = Comics
    template_name = 'profile_comics_detail.html'
