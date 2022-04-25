from django import forms
from .models import Category
from .models import News
import re
from django.core.exceptions import ValidationError


# форма с привязкой к модели
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'is_published', 'category', 'photo']  # или '__all__'
        # виджеты(по сути стили css) в отличии от непривязанной модели приписываются в словарь
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    # собственный валидатор, например будем проверять чтобы title не начинался с цифры
    # метод отработает автоматически при вызове is_valid() в views
    # имя функции-валидатора должно начинаться с clean_название_поля
    def clean_title(self):
        # в self.cleaned_data находится словарь с данными из формы, вытягиваем title по ключу и проверяем
        title = self.cleaned_data['title']
        # с помощью ругялрки проверям не начинается ли строка с цифры, если да то возбуждаем исключение
        if re.match(r'\d', title):
            raise ValidationError('Наименование не должно начинаться с цифры')
        # если все ок возвращаем строку
        else:
            return title

    # проверяем проставлена ли галочка в пункте Опубликовано в форме
    def clean_is_published(self):
        is_published = self.cleaned_data['is_published']
        if is_published:
            return is_published
        else:
            raise ValidationError('Новость должна быть опубликована')

# форма, без привязки к модели, описываем каждое поле вручную
# class NewsForm(forms.Form):
#     title = forms.CharField(max_length=150, label='Название:',
#                             widget=forms.TextInput(attrs={'class': 'form-control'}))
#     content = forms.CharField(label='Текст:', required=False,
#                               widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
#     is_published = forms.BooleanField(label='Опубликовано:', initial=True)
#     category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория:',
#                                       empty_label='Выберите категорию',
#                                       widget=forms.Select(attrs={'class': 'form-control'}))
