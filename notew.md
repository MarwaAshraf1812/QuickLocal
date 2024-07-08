Product App Overview with New Features
Initial Setup:

Created models for Product, SubCategory, and Category.
Fields for name, description, price, category, stock, and timestamps.
Added image field to Product model for handling product images.
Implemented tagging feature using django-taggit for flexible product categorization.
Custom image upload path function for organizing uploaded images.
Implemented serializers to convert Product, SubCategory, and Category models to JSON and vice versa, including support for images and tags.
Configured viewsets for CRUD operations on Product, SubCategory, and Category models using Django REST Framework.
Defined API endpoints for Product, SubCategory, and Category listing, details, delete, update, including image and tag handling.
Updated settings to handle media files and configured URLs for serving media during development.
Prepared for future enhancements with structured API endpoints and clear separation of concerns.
New Features:

Nested Subcategories and Products:

Extended models to include SubCategory as a separate model related to Category.
Each Category can have multiple SubCategories, and each SubCategory can have multiple Products.
Enhanced Serializers:

Updated serializers to handle nested relationships.
CategorySerializer now includes a nested representation of SubCategories.
SubCategorySerializer includes a nested representation of Products.
Prefetch Related Data:

Optimized database queries by using prefetch_related in viewsets to reduce the number of queries when fetching related data.
Detailed API Endpoints:

Added endpoints to retrieve all subcategories under a specific category.
Added endpoints to retrieve all products under a specific subcategory.
Viewsets and URLs:

Updated viewsets to handle nested routes for subcategories and products.
Configured URLs to support nested resource fetching.

## https://medium.com/swlh/searching-in-django-rest-framework-45aad62e7782
>> helped me in search part
