from django.db import models
from django.urls import reverse


# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True,
                              verbose_name='Фото')  # разбиваем файлы по дате загрузке
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория',
                                 related_name='get_news')
    views = models.IntegerField(default=0)
    # related_name - имя обратного отношения к первичной модели. Category - первичная, News - вторичная.
    # Category.objects.get(pk=1).news_set.all() - получим все записи из модели News, которые принадлежат категории
    # pk=1, news_set  - имя по умолчанию, созданное Django, для удобства его можно изменить через related_name.

    def __str__(self):
        return self.title

    # Генерируем ссылку через функцию, news = название шаблона в news/urls.
    # ссылка вида /news/id/
    def get_absolute_url(self):
        return reverse('news', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')

    def __str__(self):
        return self.title

    # Генерируем ссылку через функцию, category = название шаблона в news/url.
    # ссылка вида /category/id/
    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']
