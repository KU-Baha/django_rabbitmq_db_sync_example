import random

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Product, User
from .producer import publish
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    def list(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        publish('product_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(instance=product)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(instance=product, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        publish('product_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        product.delete()
        publish('product_deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            "id": user.id
        })