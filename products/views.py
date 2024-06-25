from rest_framework import viewsets # type: ignore
from django.shortcuts import render
from .models import Product, Category, Order, OrderItem
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, OrderItemSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def list(self, request):
    #     products = self.get_queryset()
    #     return render(request, 'product_list.html', {'products': products})

    # def retrieve(self, request, pk=None):
    #     product = self.get_object()
    #     return render(request, 'product_detail.html', {'product': product})

class ProductDetailsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # def list(self, request):
    #     categories = self.get_queryset()
    #     return render(request, 'category_list.html', {'categories': categories})
    
    # def retrieve(self, request, pk=None):
    #     category = self.get_object()
    #     return render(request, 'category_detail.html', {'category': category})
    

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # def list(self, request):
    #     orders = self.get_queryset()
    #     return render(request, 'order_list.html', {'orders': orders})
    
    # def retrieve(self, request, pk=None):
    #     order = self.get_object()
    #     return render(request, 'order_detail.html', {'order': order})

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
