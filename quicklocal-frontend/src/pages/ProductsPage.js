import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import apiService from '../services/apiService';

const ProductsPage = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const location = useLocation();

    useEffect(() => {
        const queryParams = new URLSearchParams(location.search);
        const categoryId = queryParams.get('category');

        if (categoryId) {
            const fetchProducts = async () => {
                try {
                    setLoading(true);
                    const response = await apiService.getProductsByCategory(categoryId);
                    console.log('Fetched Products:', response); // Debug API response
                    setProducts(response.products); // Extract the products array from the response
                    setLoading(false);
                } catch (error) {
                    setError("Failed to load products");
                    setLoading(false);
                }
            };
            fetchProducts();
        } else {
            setLoading(false);
        }
    }, [location.search]);

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }
    const baseUrl = 'http://127.0.0.1:8000';

    return (
        <div className="container my-5">
        <h2 className="text-center mb-4">Products</h2>
        <div className="row">
            {products.map(product => (
                <div key={product.id} className="col-md-4 col-lg-3 mb-4">
                    <div className="card products-card shadow-sm border-light">
                        <img
                            src={`${baseUrl}${product.image}`}
                            alt={product.name}
                            className="card-img-top products-image"
                            onError={(e) => {
                                console.error(`Image failed to load: ${e.target.src}`);
                                e.target.src = '/path/to/fallback-image.jpg'; // Fallback image URL
                            }}
                        />
                        <div className="cards-body text-center">
                            <h5 className="cards-title">{product.name}</h5>
                            <p className="card-text">${product.price}</p>
                            <a href={`/product/${product.id}`} className="btn btn-primary">View Details</a>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    </div>
    );
};

export default ProductsPage;
