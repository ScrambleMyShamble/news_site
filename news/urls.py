from django.urls import path
from .views import HomeNewsList, CategoryNewsList, DetailNews, CreateNews
# index, get_category, get_news, add_news, test_paginate
from django.views.decorators.cache import cache_page


urlpatterns = [
    # маршруты представлений через функции
    # path('', index, name='home')
    # path('category/<int:category_id>/', get_category, name='category')
    # path('news/<int:news_id>/', get_news, name='news'),
    # path('news/add_news/', add_news, name='add_news'),
    # тест пагинации через функцию
    #path('test/', test_paginate, name='paginate'),


    # маршруты представлений через классы
    # path('', cache_page(60)(HomeNewsList.as_view()), name='home'), вариант с кешированием
    path('', HomeNewsList.as_view(), name='home'),
    path('category/<int:category_id>/', CategoryNewsList.as_view(), name='category'),
    path('news/<int:pk>/', DetailNews.as_view(), name='news'),
    path('news/add_news/', CreateNews.as_view(), name='add_news'),
]
