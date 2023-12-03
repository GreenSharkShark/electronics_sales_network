from rest_framework.serializers import ValidationError
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

    def perform_update(self, serializer):
        object_to_update = self.get_object()
        updated_debt_to_the_supplier = serializer.validated_data.get('debt_to_the_supplier')

        if updated_debt_to_the_supplier and updated_debt_to_the_supplier != object_to_update.debt_to_the_supplier:
            raise ValidationError(
                {'error': 'Изменение обновления задолженности перед поставщиком через обращение к API запрещено'}
            )
        super().perform_update(serializer)
