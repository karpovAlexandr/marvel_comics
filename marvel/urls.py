from django.urls import path

from marvel.views import (
    ComicsDetailView, ComicsListAPIView,
    ComicsCreateView, ComicsUpdateView,
    UserLoginView, UserLogOutView
)

app_name = 'marvel'

urlpatterns = (
    path('marvel/', ComicsListAPIView.as_view(), name='comics_list'),
    path('marvel/comics/<int:comic_id>', ComicsDetailView.as_view(), name='comics_detail'),
    path('marvel/comics/<int:comic_id>/create', ComicsCreateView.as_view(), name='comics_create'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogOutView.as_view(), name='logout')

)
