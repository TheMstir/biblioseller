from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView
from .models import Library
from .forms import LibraryForm


class LibraryListView(ListView):
    template_name = 'mainlib/library_list.html'
    context_object_name = 'books'
    queryset = Library.objects.filter(archived=False)


class LibDetailsView(DetailView):
    """Представление для просмотра детализации книжки"""
    template_name = "mainlib/lib_detail.html"
    model = Library
    context_object_name = "book"


class LibUpdateView(UpdateView):
    model = Library
    fields = "tittle", "price", "description", "stock",
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "mainlib:lib-detail",
            kwargs={"pk": self.object.pk},
        )


def create_library(request):
    if request.method == 'POST':
        form = LibraryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mainlib/library_list.html')  # перенаправление на страницу со списком библиотек
    else:
        form = LibraryForm()
    return render(request, 'mainlib/create_new_book.html', {'form': form})
