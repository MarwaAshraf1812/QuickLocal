# Description: This file contains helper functions for the products app.

def apply_product_filters(products, params):
    category = params.get('category')
    name = params.get('name')
    price_min = params.get('min_price')
    price_max = params.get('max_price')
    rating = params.get('rating')
    tags = params.getlist('tags')


    if category:
        similar_products = products.filter(category__name__icontains=category)
    if name:
        similar_products = products.filter(name__icontains=name)
    if price_min:
        similar_products = products.filter(price__gte=price_min)
    if price_max:
        similar_products = products.filter(price__lte=price_max)
    if rating:
        similar_products = products.filter(rating__gte=rating)
    if tags:
        for tag in tags:
            similar_products = products.filter(tags__name=tag)

    return similar_products