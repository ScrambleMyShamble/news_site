from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import News, Category
from .forms import NewsForm
from .utils import MyMixin


#                                   Отображения через классы

class HomeNewsList(MyMixin, ListView):
    # шаблон через класс формируется автоматически по названию приложения и модели + _list.html
    # для этого класса шаблон будет - news/news_list.html
    # данные, которые передаются в шаблон, хранятся по умолчанию в переменной object_list
    model = News  # по аналогии news = News.objects.all() в def index
    # переопределяем название шаблона
    template_name = 'news/home_news_list.html'
    # переопределяем название переменной, в которой хранятся передаваемые данные в шаблон
    context_object_name = 'news'
    # оптимизация запроса к БД
    # queryset = News.objects.select_related('category')
    mixin_prop = 'hello world'
    # по умолчанию в html передается объект пагинации с именем page_obj
    paginate_by = 3

    # передаем дополнительные переменные, в extra_context передаются только статичные данные
    # или написать специальный метод get_context_data
    # extra_context = {'title': 'Главная страница'}

    # метод get_context_data нужен для передачи через него дополнительных данных, помимо передаваемых по умолчанию
    # из ListView, например object_list создается и передается по умолчанию.
    # родительский метод get_context_data возвращает словарь context с данными, мы должны опеделить его
    # в нашем методе через super, после чего уже добавить всю нужную дополнительную информацию, как в словарь
    def get_context_data(self, *, object_list=None, **kwargs):
        # в context уже заложена базовая информация из родительского метода
        context = super().get_context_data(**kwargs)
        # дополняем context нужными данными
        # self.get_upper работа с mixin из utils
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    # метод-фильтр для главной страницы, выводим только опубликованные новости
    # применяется queryset.filter
    def get_queryset(self):
        # оптимизация запроса на главной странице, через select_related будет 4 запроса к БД.
        # select_related подходит когда связь через foreign key, category в News это foreign key на модель
        # category, если manytomany используется prefetch_related
        # при select_related django грузит сразу все категории в карточках новостях при загрузке главной страницы
        # можно прописать в методе или в атрибутах класса
        return News.objects.filter(is_published=True).select_related('category')
        # при таком - 20
        # return News.objects.filter(is_published=True)


class CategoryNewsList(MyMixin, ListView):
    model = News
    # шаблон по умолчанию news/news_list.html
    template_name = 'news/category.html'
    context_object_name = 'news'
    # не показываем пустые списки, т.е. если пытаемся получить категорию которой не существует выдаст 404 ошибку
    # а не 500. Или категория существует но в ней нет новостей, так же выдаст 404 ошибку.
    allow_empty = False
    paginate_by = 3
    # метод фильтр для отображения всех новостей по категориям
    def get_queryset(self):
        # print(self.kwargs['category_id'])
        # is_published=True  отобразятся только опубликованные новости.
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    # описал выше
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.get_upper работа с mixin из utils
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context


class DetailNews(DetailView):
    model = News
    # к объекту можно обращаться либо по pk, либо по slug, в url передается news_id, можно указать что pk
    # приходит в виде параметра news_id, с помощью встроенной переменной pk_url_kwarg
    # но лучшая практика, по умолчанию передать pk, поэтому в url меняем на pk. Больше ничего делать не надо.
    # pk_url_kwarg = 'news_id'
    # шаблон по умолчанию news/news_detail.html
    template_name = 'news/news_view.html'
    # по умолчанию переменная с данными, передаваемыми в шаблон, называется object
    context_object_name = 'news'


class CreateNews(LoginRequiredMixin, CreateView):
    # связываем класс с формой, в которую вводятся данные для создания
    form_class = NewsForm
    # шаблон по умолчанию news/news_form.html
    template_name = 'news/add_news.html'
    # после добавления новости по прежнему происходит redirect на подробную страницу созданной новости,
    # происходит это за счет того, что в модели News прописан метод get_absolute_url
    # переопределяем redirect в самом view классе, а не через модель, reverse здесь не работает в отличие от модели,
    # применяется reverse_lazy.
    # success_url = reverse_lazy('home')

    # если пользователь не прошел аутентификацию и хочет добавить новость, перенаправляем на домашнюю страницу
    login_url = reverse_lazy('home')
    # или через переменную raise_exception выдать 403 ошибку, доступ запрещен
    raise_exception = True


#                                      Отображения через функции


# пагинация через функцию
# def test_paginate(request):
#     news_list = News.objects.all()
#     paginator = Paginator(news_list, 5)
#     # если страницы в GET массиве нет, передаем значение по умолчанию = 1
#     page_number = request.GET.get('page', 1)
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'news/test.html', {'page_obj': page_obj})


# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, 'news/index.html', context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news': news, 'category': category})


# def get_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/news_view.html', {'news': news_item})


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # в cleaned_data содержится информация из reqeust.POST в формате python-словаря.
#             # распаковываем его, и каждому атрибуту из модели News присвоится значение из словаря.
#             # т.к. метод create возвращает объект созданной записи, можно сохранить его в переменную
#             # create и распаковка словаря используются если форма не привязана к модели
#             # news = News.objects.create(**form.cleaned_data)
#             # если форма привязана к модели используется только метод save()
#             news = form.save()
#             # redirect на подробную страницу с этой новостью
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})
