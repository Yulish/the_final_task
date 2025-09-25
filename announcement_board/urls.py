from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from board.views import (PosterList, PosterDetail, PosterCategory, PosterAdd, ResponseCreate,
                         register_view, verify_code_view, custom_upload, ResponseAccept,
                         ResponseList, ResponseDetail, AcceptedResponses, ResponseDelete,
                         ProfileView, ProfileUpdate, PosterDelete, PosterChange, StartView,
                         my_logout)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', StartView.as_view(), name='start_page'),
    path('accounts/', include('allauth.urls')),
    path('logout/', my_logout, name='my_logout'),
    path('users/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('users/<int:pk>/update/', ProfileUpdate.as_view(), name='profile_update'),
    path('register/', register_view, name='register'),
    path('verify/<int:user_id>/', verify_code_view, name='verify_code'),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('posters/', PosterList.as_view(), name='posters'),
    path('create/', PosterAdd.as_view(), name='create'),
    path('posters/<int:pk>/', PosterDetail.as_view(), name='poster_detail'),
    path('posters/<int:pk>/delete', PosterDelete.as_view(), name='poster_delete'),
    path('posters/<int:pk>/update/', PosterChange.as_view(), name = 'poster_update'),
    path('users/<int:pk>/responses/search', ResponseList.as_view(), name='responses'),
    path('posters/<int:pk>/response', ResponseCreate.as_view(), name='response'),
    path('responses/<int:pk>/', ResponseDetail.as_view(), name='response_detail'),
    path('responses/<int:pk>/accept/', ResponseAccept.as_view(), name='response_accept'),
    path('responses/accepted/', AcceptedResponses.as_view(), name='accepted_responses'),
    path('responses/<int:pk>/delete/', ResponseDelete.as_view(), name='response_delete'),
    path('categories/<int:pk>/', PosterCategory.as_view(), name='category_list'),
    path('ckeditor/upload/', custom_upload, name='ckeditor_upload'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)