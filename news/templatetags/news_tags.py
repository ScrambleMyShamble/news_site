from django import template
from news.models import Category, News
from news.utils import MyMixin
from django.db.models import *


''' Создание собственного тега шаблона '''

register = template.Library()


# Можно будет отбращаться к данной функции из любого html-документа, для получения тега
# в нашем случае для получения Category.objects.all()
# в html_документе тег доступен по имени созданной функции {% get_categories %}, в html документе требуется только
# загрузить данный тег {% load news_tags %}, по имени созданного модуля.
@register.simple_tag()  # декоратор для того, чтобы зарегистрировать функцию в теги шаблона
def get_categories():
    # аггрегирование аннотаций -> документация.
    # показываем категории в которых количество новостей больше 0(cnt__gt=0)
    # после этого у каждого объекта создается атрибут cnt(кол-во), которое можно выводить на странице,
    # вывод будет количество новостей по каждой категории в блоке категорий.
    category_list = Category.objects.annotate(cnt=Count('get_news')).filter(cnt__gt=0)
    # передаем в _sidebar.html, для отображения всех существующих категорий, у которых новостей больше 0(cnt__gt)
    return category_list


# inclusion_tag работает через рендеринг страницы, после чего передается в переменную, страница создается
# и передается в параметры inclusion_tag(путь к html странице которая будет рендерить)
# @register.inclusion_tag('news/list_categories.html')
# def show_categories():
#     categories = Category.objects.all()
#     return {'categories': categories} # на выходе будет словарь и не queryset, за счет рендера через
#                                         list_categories.html - страница-рендер
