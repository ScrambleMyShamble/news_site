from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import News, Category


# Register your models here.


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published', 'get_photo', 'views')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    # список полей, которые будут отображаться внутри новости, если указать в этом списке поля, которые нельзя
    # редактировать, выдаст ошибку, доп. в переменной readonly_fields нужно внести эти нередактируемые поля.
    fields = ('title', 'category', 'content', 'photo', 'get_photo',
              'is_published', 'views', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at', 'get_photo', 'views')

    # obj - объект записи с атрибутами
    # выводим фото в админке, в list_display прописывается метод
    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return 'Фото не выбрано'

    # меняем название поля в админке на читаемое, если не указать явно выводится имя метода get_photo
    get_photo.short_description = 'Фото'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.site_title = 'Управление новостями'
admin.site.site_header = 'Управление новостями'
