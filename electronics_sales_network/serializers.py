from rest_framework import serializers
from electronics_sales_network.models import ChainLink
from electronics_sales_network.validators import ChainLinkValidator


class ChainLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChainLink
        fields = '__all__'

    def validate(self, data):
        validator = ChainLinkValidator(data)
        validator()

        return data
