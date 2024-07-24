from rest_framework import serializers #type: ignore
from .models import Category, SubCategory, Product

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())

    class Meta:
        model = Product
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = '__all__'
    
    def get_products(self, obj):
        products = obj.products.all()
        return ProductSerializer(products, many=True).data

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        return SubCategorySerializer(subcategories, many=True).data