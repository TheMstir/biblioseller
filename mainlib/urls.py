from django.urls import path
from .views import (
    LibraryListView,
    create_library,
    LibUpdateView,
    LibDetailsView,
    index,
    add_image,
    add_money)

app_name = "mainlib"

urlpatterns = [
    path('', index, name='index'),
    path('list/', LibraryListView.as_view(), name='lib-list'),
    path('create/', create_library, name='create-book'),
    path('list/<int:pk>/', LibDetailsView.as_view(), name="book-details"),
    path('list/<int:pk>/update/', LibUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/add_image/', add_image, name='add_image'),
    path('add_money/', add_money, name='add_money'),
]

