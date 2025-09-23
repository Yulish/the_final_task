from django_filters import FilterSet
from .models import Poster, Response, Category
import django_filters
from django import forms



class PosterFilter(FilterSet):

    author_username = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains', label='Автор объявления')
    head = django_filters.CharFilter(lookup_expr='icontains', label='Название объявления')
    text = django_filters.CharFilter(lookup_expr='icontains', label='Текст объявления')
    date_from = django_filters.DateFilter(
        field_name='poster_origin',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Показать объявления после даты'
    )
    categories = django_filters.ModelChoiceFilter(
        # field_name='poster__categories',
        queryset=Category.objects.all(),
        label='Категория',
        required=False,
        empty_label='Все категории',
        widget=forms.Select(attrs={
            'style': 'width: 200px;',
        })
    )
    class Meta:
        model = Poster
        fields = []

class ResponseFilter(django_filters.FilterSet):
    sender_username = django_filters.CharFilter(
        field_name='sender__username',  # sender — поле User в Response
        lookup_expr='icontains',
        label='Автор отклика'
    )
    head = django_filters.CharFilter(
        field_name='poster__head',
        lookup_expr='icontains',
        label='Название объявления'
    )

    categories = django_filters.ModelChoiceFilter(
        field_name='poster__categories',
        queryset=Category.objects.all(),
        label='Категория',
        required=False,
        empty_label='Все категории',
        widget=forms.Select(attrs={
            'style': 'width: 200px;',
        })
    )
    class Meta:
        model = Response
        fields = []