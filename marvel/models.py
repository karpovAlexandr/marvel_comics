from django.contrib.auth.models import User
from django.db import models


class Images(models.Model):
    """Модель для поля images"""
    image_url = models.ImageField()

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Characters(models.Model):
    """Модель Персонажа"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    resource_uri = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Персонаж'
        verbose_name_plural = 'Персонажи'


class Creators(models.Model):
    """Модель Автора"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    resource_uri = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Создатель'
        verbose_name_plural = 'Создатели'


class Stories(models.Model):
    """Модель Истории"""
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    resource_uri = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'Истории'


class Comics(models.Model):
    """Модель комикса
    https://developer.marvel.com/docs#!/public/getComicsCollection_get_6
    """
    comics_id = models.IntegerField()
    digital_id = models.IntegerField()
    title = models.CharField(max_length=250)
    issue_number = models.IntegerField()
    variant_description = models.CharField(max_length=500, blank=True)
    description = models.TextField(null=True)
    modified = models.DateTimeField()
    isbn = models.CharField(max_length=50, default=None)
    upc = models.CharField(max_length=50, default=None)
    diamond_code = models.CharField(max_length=50)
    ean = models.CharField(max_length=50)
    issn = models.CharField(max_length=50)
    format = models.CharField(max_length=50)
    page_count = models.SmallIntegerField()
    text_objects = models.JSONField()
    resource_uri = models.URLField()
    urls = models.JSONField()
    series_resource_uri = models.CharField(max_length=500)
    series_name = models.CharField(max_length=100)
    variants = models.JSONField()
    collections = models.JSONField()
    collected_issues = models.JSONField()
    dates = models.JSONField()
    prices = models.JSONField()
    thumbnail = models.ImageField()
    images = models.ManyToManyField(Images)
    creators = models.ManyToManyField(Creators)
    characters = models.ManyToManyField(Characters)
    stories = models.ManyToManyField(Stories)
    events = models.JSONField()

    def __str__(self):
        return f'{self.comics_id} - {self.title}'

    class Meta:
        verbose_name = 'Комикс'
        verbose_name_plural = 'Комиксы'


class Profile(models.Model):
    """Модель пользователя с привязкой к приюту"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    comics = models.ManyToManyField(Comics, blank=True)

    def __str__(self):
        return f"Профайл пользователя - {self.user.username}"

    class Meta:
        verbose_name = 'Профайл'
        verbose_name_plural = 'Профайлы'
