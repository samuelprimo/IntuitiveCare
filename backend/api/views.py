from rest_framework import generics
from api.serializers import OperadoraSerializer
from api.models import Operadora
from api.filters import OperadoraFilter


class OperadoraViewList(generics.ListAPIView):
    queryset = Operadora.objects.all()
    serializer_class = OperadoraSerializer
    filterset_class = OperadoraFilter
