from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView
from .models import Library
from .forms import LibraryForm


class LibraryListView(ListView):
    """Представление для просмотра всех книг списком"""
    template_name = 'mainlib/library_list.html'
    context_object_name = 'books'
    queryset = Library.objects.filter(archived=False)

    def get_queryset(self):
        """Форма поиска"""
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(title__icontains=q)
        return queryset


class LibDetailsView(DetailView):
    """Представление для просмотра детализации книжки"""
    template_name = "mainlib/lib_detail.html"
    model = Library
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        """Добавляет возможность подключения разных дополнительных изображений"""
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        return context


class LibUpdateView(UpdateView):
    model = Library
    fields = "tittle", "price", "description", "stock", 'image', 'in_pc_link', 'in_room_place'
    context_object_name = "book"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "mainlib:book-details",
            kwargs={"pk": self.object.pk},
        )


def create_library(request):
    if request.method == 'POST':
        form = LibraryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mainlib:lib-list')  # перенаправление на страницу со списком библиотек
    else:
        form = LibraryForm()
    return render(request, 'mainlib/create_new_book.html', {'form': form})


def index(request):
    return render(request, 'mainlib/main.html', {})