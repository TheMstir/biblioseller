from django.db import models

def image_directory_path(instance, filename):
    """функция для направления подгружаемых картинок в папку"""
    return f"books/{instance.category}/{filename}"


class Category(models.Model):
    """
    Модель для категоризации списка книг
    """
    title = models.CharField(max_length=150)


class Library(models.Model):
    """
    Модель для хранения базы различных книжек

    sale: учитывает количество проданных копий, для формирования списка популярности

    archived: применяется для того чтобы временно убрать книжку из отображения
    """

    tittle = models.CharField(max_length=100, verbose_name='название')
    description = models.TextField(null=False, blank=True, verbose_name='описание')
    image = models.ImageField(upload_to=image_directory_path, default='', blank=True, verbose_name='изобрадение')
    stock = models.IntegerField(default=0, null=False, verbose_name="запасы")
    sale = models.IntegerField(default=0, null=True, verbose_name="продано")
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, null=False, verbose_name="цена")
    in_pc_link = models.TextField(verbose_name='ссылка на версию в хранилище')
    in_room_place = models.TextField(verbose_name='примерное расположение в доме')
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False, verbose_name='архивная')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="books", verbose_name="категория")

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return f"Книжка {self.tittle}, остаток {self.stock}"

    # нужен сервис истории цены, куда складывается история изменения цены на продукт


class LibImages(models.Model):
    """
    Модель для хранения списка изображений под отдельную книжку
    для быстрого ответа на вопрос о качестве книги
    связывается с книгой по ключу
    """
    name = models.CharField(
        max_length=48, null=False, blank=True, verbose_name="описывающий текст"
    )
    product = models.ForeignKey(
        Library, on_delete=models.CASCADE, related_name="images", verbose_name="книга"
    )
    image = models.FileField(
        upload_to=image_directory_path, verbose_name="путь к изображению"
    )

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def src(self):
        return self.image

    def __str__(self):
        return f"/{self.image}"


class LibTags(models.Model):
    """
    Модель для хранения связывающих тэгов
    так же подрузамевается хранение расхожих проблем, связанных с книжками
    """

    book = models.ForeignKey(Library, on_delete=models.PROTECT)
    tag = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.tag



