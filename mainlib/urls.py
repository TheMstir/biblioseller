from django.urls import path
from .views import LibraryListView, create_library, LibUpdateView, LibDetailsView

app_name = "mainlib"

urlpatterns = [
    path('list/', LibraryListView.as_view(), name='lib-list'),
    path('create/', create_library, name='create-book'),
    path('list/<int:pk>/', LibDetailsView.as_view(), name="book-details"),
    path('list/<int:pk>/update/', LibUpdateView.as_view(), name='book-update'),
]

