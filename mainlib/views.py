from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView
from .models import Library, Money, LibImages
from .forms import LibraryForm, LibImagesForm, MoneyForm
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


class LibraryListView(ListView):
    """Представление для просмотра всех книг списком"""
    template_name = 'mainlib/library_list.html'
    context_object_name = 'books'
    queryset = Library.objects.filter(archived=False)
    paginate_by = 20  # количество объектов на странице

    def get_queryset(self):
        """Форма поиска"""
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(tittle__icontains=q)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(context['books'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


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
        form = LibraryForm(request.POST, request.FILES)
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
            return redirect('mainlib:book-details', pk=book.pk)
    else:
        form = LibImagesForm()
    return render(request, 'mainlib/add_image.html', {'form': form})


def add_money(request):
    if request.method == 'POST':
        form = MoneyForm(request.POST)
        if form.is_valid():
            money = form.save(commit=False)
            money.mounth += Money.objects.last().mounth + money.now
            money.save()
            # Обнуляем mounth каждые 30 дней
            last_month = Money.objects.last().mounth
            if last_month + 30 <= datetime.now().day:
                # Только сначала доход месяца перекидываем в общий
                money.all += money.mounth
                Money.objects.all().update(mounth=0)

            return redirect('mainlib:index')
    else:
        form = MoneyForm()
    return render(request, 'mainlib/add_money.html', {'form': form})


def index(request):
    money = Money.objects.last()  # получаем первый объект из модели Money
    context = {'money': money}

    return render(request, 'mainlib/main.html', context)

@csrf_exempt
def delete_image_view(request):
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        try:
            image = LibImages.objects.get(id=image_id)
            image.delete()
            return JsonResponse({'success': True})
        except LibImages.DoesNotExist:
            pass
    return JsonResponse({'success': False})