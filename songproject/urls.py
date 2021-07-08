
from django.contrib import admin
from django.urls import path
from songs.views import AlbumList, AlbumDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('album/', AlbumList.as_view()),
    path('album/<int:pk>/', AlbumDetail.as_view()),
]
