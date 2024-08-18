import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import apiService from '../services/apiService';
import './CategoriesPage.css';

const CategoriesPage = () => {
    // States for categories, loading, and error
    const [categories, setCategories] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    // Fetching data from API
    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const data = await apiService.getCategories();
                setCategories(data);
                setLoading(false);
            } catch (error) {
                setError("Failed to load data");
                setLoading(false);
            }
        };
        fetchCategories();
    }, []);

    if (loading) {
        return <p>Loading...</p>;
    }

    const handleCategoryClick = (categoryId) => {
        navigate(`/category-products/?category=${categoryId}`);
    };

    if (error) {
        return <p>{error}</p>;
    }

    return (
        <div className="categories container my-5">
            <h2 className="text-center mb-5">Categories</h2>
            <div className="row ">
                {categories.map(category => (
                    <div key={category.id} className="col-md-4 mb-5">
                        <div className="card categories-card shadow-sm border-light">
                            <img
                                src={category.image}
                                alt={category.name}
                                className="card-img-top categories-image"
                            />
                            <div className="card-body text-center">
                                <h5 className="card-title mb-4">{category.name}</h5>
                                <button
                                    className="btn btn-primary categories-button"
                                    onClick={() => handleCategoryClick(category.id)}
                                >
                                    View Products
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CategoriesPage;
