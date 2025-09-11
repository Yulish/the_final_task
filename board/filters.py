from django_filters import FilterSet
from .models import Poster, Response
import django_filters
from django import forms



class PosterFilter(FilterSet):

    author_username = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains', label='Фамилия автора')
    # head = django_filters.CharFilter(lookup_expr='icontains', label='Название объявления')
    date_from = django_filters.DateFilter(
        field_name='poster_origin',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Показать объявления после даты'
    )

    class Meta:
        model = Poster
        fields = []

class ResponseFilter(django_filters.FilterSet):
    sender_username = django_filters.CharFilter(
        field_name='sender__username',  # sender — поле User в Response
        lookup_expr='icontains',
        label='Фамилия автора'
    )
    head = django_filters.CharFilter(
        field_name='poster__head',  # поле head из связанного Poster
        lookup_expr='icontains',
        label='Название объявления'
    )
    categories = django_filters.CharFilter(
        field_name='poster__categories__name',  # поле name из связанной категории Poster
        lookup_expr='icontains',
        label='Категория'
    )
    date_from = django_filters.DateFilter(
        field_name='response_origin',
        lookup_expr='gte',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Показать отклики после даты'
    )

    class Meta:
        model = Response
        fields = []