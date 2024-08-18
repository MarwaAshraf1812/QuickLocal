import React, { useState, useEffect } from 'react';
import './ProductsSection.css';
import apiService from '../services/apiService';

const ProductsSection = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const data = await apiService.getProducts();
                setProducts(data);
                setLoading(false);
            } catch (error) {
                setError("Failed to load products");
                setLoading(false);
            }
        };
        fetchProducts();
    }, []);

    if (loading) {
        return <p>Loading...</p>;
    }
    if (error) {
        return <p>{error}</p>;
    }

    // Limit to 12 products (6 per row * 2 rows)
    const displayedProducts = products.slice(0, 12);

    return (
        <div className="container-fluid my-4">
            <h2 className="text-left mb-5">Products</h2>
            <div className="row">
                {displayedProducts.map(product => (
                    <div key={product.id} className="col-md-2 mb-4">
                        <div className="card product-card">
                            <img
                                src={product.image}
                                alt={product.name}
                                className="card-img-top product-image"
                                onError={(e) => {
                                    console.error(`Image failed to load: ${e.target.src}`);
                                    e.target.src = 'fallback-image-url.jpg'; // Replace with your fallback image URL
                                }}
                            />
                            <div className="product-card-overlay">
                                <h5 className="card-title">{product.name}</h5>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ProductsSection;
