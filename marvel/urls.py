from django.urls import path

from marvel.views import (
    ComicsCreateView, ComicsDetailView, ComicsDeleteView, ComicsListAPIView,
    ComicsUpdateView, home_page, ProfileComicsDetail,
    ProfileComicsList, UserLoginView, UserLogOutView,
)

app_name = 'marvel'

urlpatterns = (
    path('', home_page, name='home'),
    path('marvel/', ComicsListAPIView.as_view(), name='comics_api_list'),
    path('marvel/comics/<int:comic_id>', ComicsDetailView.as_view(), name='comics_api_detail'),
    path('marvel/comics/<int:comic_id>/create', ComicsCreateView.as_view(), name='comics_create'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogOutView.as_view(), name='logout'),
    path('master/', ProfileComicsList.as_view(), name='master_list'),
    path('master/<int:pk>/', ProfileComicsDetail.as_view(), name='master_detail'),
    path('master/<int:pk>/edit', ComicsUpdateView.as_view(), name='master_edit'),
    path('master/<int:pk>/delete', ComicsDeleteView.as_view(), name='master_delete'),

)
