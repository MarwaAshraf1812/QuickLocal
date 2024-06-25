from .models import Product
from rest_framework.response import Response # type: ignore
from serializers import ProductSerializer
from rest_framework.views import APIView # type: ignore

class ProductList(APIView):
    def get(self, request):
        all_products = Product.objects.all()
        data = ProductSerializer(all_products, many=True).data
        return Response(data)
    
    def put(self, request):
        all_products = Product.objects.all()
        data = ProductSerializer(all_products, data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data, status=201)
        return Response(data.errors, status=400)
    
    def delete(self, request):
        all_products = Product.objects.all()
        all_products.delete()
        return Response(status=204)
    
class Product(APIView):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        data = ProductSerializer(product).data
        return Response(data)
    
    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=204)
    
    def post(self, request):
        data = ProductSerializer(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data, status=201)
        return Response(data.errors, status=400)
    

    