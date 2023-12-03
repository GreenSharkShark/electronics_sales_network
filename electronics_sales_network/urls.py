from django.urls import path
from electronics_sales_network.apps import ElectronicsSalesNetworkConfig
from electronics_sales_network.views import ChainLinkViewSet
from rest_framework.routers import DefaultRouter


app_name = ElectronicsSalesNetworkConfig.name

router = DefaultRouter()
router.register(r'chains', ChainLinkViewSet, basename='chains')


urlpatterns = [] + router.urls
