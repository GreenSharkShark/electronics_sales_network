from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from electronics_sales_network.models import ChainLink
from electronics_sales_network.permissions import IsActiveStaff
from electronics_sales_network.serializers import ChainLinkSerializer
from rest_framework.permissions import IsAuthenticated


class ChainLinkViewSet(ModelViewSet):
    serializer_class = ChainLinkSerializer
    queryset = ChainLink.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['contacts__city']
    permission_classes = [IsAuthenticated, IsActiveStaff]
