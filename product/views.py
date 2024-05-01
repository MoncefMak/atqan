from rest_framework.generics import CreateAPIView

from product.client_permissions import CreateProductPermission
from product.models import Product
from product.serializers import ProductSerializer


class ProductCreateApiView(CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [CreateProductPermission]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
