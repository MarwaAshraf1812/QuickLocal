import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import apiService from '../services/apiService';
import AsideFilters from '../components/AsideFilters';
import './ProductsPage.css';

const ProductsPage = () => {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const location = useLocation();

    const handleFilterChange = async (filters) => {
        try {
            setLoading(true);
            const categoryId = new URLSearchParams(location.search).get('category');
            const response = await apiService.getProductsByCategory(categoryId, filters);
            setProducts(response.products);
            setLoading(false);
        } catch (error) {
            setError("Failed to load products");
            setLoading(false);
        }
    };

    useEffect(() => {
        const queryParams = new URLSearchParams(location.search);
        const categoryId = queryParams.get('category');

        if (categoryId) {
            const fetchProducts = async () => {
                try {
                    setLoading(true);
                    const response = await apiService.getProductsByCategory(categoryId);
                    console.log('Fetched Products:', response);
                    setProducts(response.products);
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
            <h2 className="text-center mb-5 fw-bold blue-color">Products</h2>
            <div className="row">
                <div className='col-md-3'>
                    <AsideFilters onFilterChange={handleFilterChange} />
                </div>
                <div className="col-md-9">
                    <div className="row">
                        {products.map(product => (
                            <div key={product.id} className="col-12 mb-4">
                                <div className="card products-card d-flex flex-row shadow-sm border-light">
                                    <div className="col-md-4 p-0">
                                        <img
                                            src={`${baseUrl}${product.image}`}
                                            alt={product.name}
                                            className="card-img-left products-image"
                                            onError={(e) => {
                                                console.error(`Image failed to load: ${e.target.src}`);
                                                e.target.src = '/path/to/fallback-image.jpg'; // Fallback image URL
                                            }}
                                        />
                                    </div>
                                    <div className="col-md-8 d-flex flex-column justify-content-center p-3">
                                        <div className="cards-body">
                                            <h5 className="cards-title align-items-start mt-2">{product.name}</h5>
                                            <p>{product.description}</p>
                                            <p className="card-text">${product.price}</p>
                                            <div className=' d-flex flex-column justify-content-center align-items-end'>
                                                <a href={`/product/${product.id}`} className="btn btn-custom-color">View Details</a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProductsPage;
