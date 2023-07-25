from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView
from .models import Library, Money
from .forms import LibraryForm, LibImagesForm, MoneyForm
from datetime import datetime, timedelta


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


def add_image(request, pk):
    """Представление позволяющее добавлять дополнительное изображение к книге"""
    book = Library.objects.get(pk=pk)
    if request.method == 'POST':
        form = LibImagesForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.product = book
            image.save()
            return redirect('mainlib:book-detail', pk=book.pk)
    else:
        form = LibImagesForm()
    return render(request, 'mainlib/add_image.html', {'form': form})


def add_money(request):
    if request.method == 'POST':
        form = MoneyForm(request.POST)
        if form.is_valid():
            money = form.save(commit=False)
            money.save()
            # Обнуляем mounth каждые 30 дней
            last_month = Money.objects.last().mounth
            if last_month + 30 <= datetime.now().day:
                Money.objects.all().update(mounth=0)
            return redirect('mainlib:main')
    else:
        form = MoneyForm()
    return render(request, 'add_money.html', {'form': form})


def index(request):
    return render(request, 'mainlib/main.html', {})