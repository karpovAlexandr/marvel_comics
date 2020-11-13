from django.contrib.auth.models import User
from django.db import models


class Images(models.Model):
    """Модель для поля images"""
    image_url = models.URLField()

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
    issue_number = models.IntegerField(blank=True)
    variant_description = models.CharField(max_length=500, blank=True)
    description = models.TextField(null=True)
    modified = models.DateTimeField()
    isbn = models.CharField(max_length=50, default=None, blank=True)
    upc = models.CharField(max_length=50, default=None, blank=True)
    diamond_code = models.CharField(max_length=50, blank=True)
    ean = models.CharField(max_length=50, blank=True)
    issn = models.CharField(max_length=50, blank=True)
    format = models.CharField(max_length=50, blank=True)
    page_count = models.SmallIntegerField(blank=True)
    text_objects = models.JSONField(blank=True)
    resource_uri = models.URLField(blank=True)
    urls = models.JSONField(blank=True)
    series_resource_uri = models.CharField(max_length=500, blank=True)
    series_name = models.CharField(max_length=100, blank=True)
    variants = models.JSONField(blank=True)
    collections = models.JSONField(blank=True)
    collected_issues = models.JSONField(blank=True)
    dates = models.JSONField(blank=True)
    prices = models.JSONField(blank=True)
    thumbnail = models.ImageField(blank=True)
    images = models.ManyToManyField(Images, blank=True)
    creators = models.ManyToManyField(Creators, blank=True)
    characters = models.ManyToManyField(Characters, blank=True)
    stories = models.ManyToManyField(Stories, blank=True)
    events = models.JSONField(blank=True)

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
