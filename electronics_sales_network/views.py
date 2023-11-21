from rest_framework import viewsets
from electronics_sales_network.models import ChainLink
from electronics_sales_network.serializers import ChainLinkSerializer


class ChainLinkViewSet(viewsets.ModelViewSet):
    serializer_class = ChainLinkSerializer
    queryset = ChainLink.objects.all()
