product app >>

Initial setup for Product app with CRUD operations, API endpoints, and media/tag handling

- Created models for Product and Category with fields for name, description, price, category, stock, and timestamps.
- Added image field to Product model for handling product images.
- Implemented tagging feature using django-taggit for flexible product categorization.
- Defined a custom image upload path function for organizing uploaded images.
- Implemented serializers to convert Product and Category models to JSON and vice versa, including support for images and tags.
- Configured viewsets for CRUD operations on Product and Category models using Django REST Framework.
- Defined API endpoints for Product and Category listing, details, delete, update, including image and tag handling.
- Updated settings to handle media files and configured URLs for serving media during development.
- Prepared for future enhancements with structured API endpoints and clear separation of concerns.
