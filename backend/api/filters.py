from rest_framework import generics
from django_filters import rest_framework as django_filters
from api.models import Operadora
from api.serializers import OperadoraSerializer


class OperadoraFilter(django_filters.FilterSet):
    nome_fantasia = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Operadora
        fields = ['nome_fantasia']