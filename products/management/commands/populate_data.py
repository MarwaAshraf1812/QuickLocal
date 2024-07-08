from django.core.management.base import BaseCommand
from products.models import Category, SubCategory, Product
from taggit.models import Tag
from django.core.files.uploadedfile import SimpleUploadedFile

class Command(BaseCommand):
    help = 'Populate database with dummy data'

    def handle(self, *args, **kwargs):
        categories_data = [
            {"name": "Electronics", "description": "Electronic items"},
            {"name": "Clothing", "description": "Men's and Women's clothing"},
            {"name": "Home", "description": "Home appliances and furniture"},
            {"name": "Books", "description": "Various books"},
            {"name": "Sports", "description": "Sporting goods"},
        ]

        subcategories_data = [
            {"name": "Mobile Phones", "category": "Electronics"},
            {"name": "Laptops", "category": "Electronics"},
            {"name": "Cameras", "category": "Electronics"},
            {"name": "Men", "category": "Clothing"},
            {"name": "Women", "category": "Clothing"},
            {"name": "Kids", "category": "Clothing"},
            {"name": "Appliances", "category": "Home"},
            {"name": "Furniture", "category": "Home"},
            {"name": "Cookware", "category": "Home"},
            {"name": "Outdoor", "category": "Home"},
            {"name": "Fitness", "category": "Sports"},
            {"name": "Team Sports", "category": "Sports"},
            {"name": "Fiction", "category": "Books"},
            {"name": "Non-Fiction", "category": "Books"},
            {"name": "Educational", "category": "Books"},
        ]

        products_data = [
            {"name": "iPhone 13", "description": "Latest model of iPhone with A15 Bionic chip.", "price": 999.99, "subcategory": "Mobile Phones"},
            {"name": "MacBook Air", "description": "Apple M1 chip with 8-core CPU.", "price": 1299.99, "subcategory": "Laptops"},
            {"name": "Nikon D3500", "description": "Beginner DSLR camera.", "price": 499.99, "subcategory": "Cameras"},
            {"name": "Men's T-Shirt", "description": "100% cotton t-shirt.", "price": 19.99, "subcategory": "Men"},
            {"name": "Women's Dress", "description": "Stylish summer dress.", "price": 39.99, "subcategory": "Women"},
            {"name": "Kids' Sneakers", "description": "Comfortable and durable sneakers for kids.", "price": 29.99, "subcategory": "Kids"},
            {"name": "Blender", "description": "High-power kitchen blender.", "price": 49.99, "subcategory": "Appliances"},
            {"name": "Sofa", "description": "Comfortable 3-seater sofa.", "price": 499.99, "subcategory": "Furniture"},
            {"name": "Non-Stick Pan", "description": "Durable non-stick frying pan.", "price": 29.99, "subcategory": "Cookware"},
            {"name": "Tent", "description": "4-person camping tent.", "price": 99.99, "subcategory": "Outdoor"},
            {"name": "Dumbbells", "description": "Set of 2 dumbbells.", "price": 59.99, "subcategory": "Fitness"},
            {"name": "Soccer Ball", "description": "Official size and weight soccer ball.", "price": 24.99, "subcategory": "Team Sports"},
            {"name": "Fiction Novel", "description": "Bestselling fiction novel.", "price": 14.99, "subcategory": "Fiction"},
            {"name": "History Book", "description": "Comprehensive history of ancient civilizations.", "price": 29.99, "subcategory": "Non-Fiction"},
            {"name": "Math Textbook", "description": "High school mathematics textbook.", "price": 39.99, "subcategory": "Educational"},
        ]

        for category_data in categories_data:
            Category.objects.get_or_create(name=category_data["name"], defaults={"description": category_data["description"]})

        for subcategory_data in subcategories_data:
            category = Category.objects.get(name=subcategory_data["category"])
            SubCategory.objects.get_or_create(name=subcategory_data["name"], category=category)

        for product_data in products_data:
            subcategory = SubCategory.objects.get(name=product_data["subcategory"])
            product, created = Product.objects.get_or_create(
                name=product_data["name"],
                description=product_data["description"],
                productInformation=f"Information about {product_data['name']}",
                price=product_data["price"],
                category=subcategory,
                defaults={
                    "stock": 100,
                    "rating": 4.5,
                    "status": 'Available',
                    "color": '#FFFFFF',
                    "size": 'M',
                    "image": SimpleUploadedFile(name=f'{product_data["name"]}.jpg', content=b'', content_type='image/jpeg')
                }
            )
            if created:
                product.tags.add('popular', 'new', 'sale')

        self.stdout.write(self.style.SUCCESS('Data creation complete.'))
