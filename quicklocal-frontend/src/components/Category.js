import React, { useState, useEffect } from "react";
import './Category.css';
import apiService from "../services/apiService";

const CategoriesSection = () => {
    //states for categories, loading and error
    const [categories, setCategories] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    //fetching data from api
    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const data = await apiService.getCategories();
                setCategories(data);
                setLoading(false);
            } catch (error) {
                setError("Faild to load data");
                setLoading(false);
            }
        };
        fetchCategories();
    }, []);

    if (loading) {
        return <p>Loading...</p>;
    }
    if (error) {
        return <p>{error}</p>;
    }

    const displayedCategories = categories.slice(0, 5);

    return (
        <div className="container-fluid my-1 category-section">
            <div className="row justify-content-center align-items-center">
                {displayedCategories.map((category) => (
                    <div key={category.id} className="col-md-2 mb-4">
                        <div className="category-card d-flex align-items-center">
                            <img
                                src={category.image}
                                alt={category.name}
                                className="img-fluid category-image"
                                onError={(e) => {
                                    console.error(`Image failed to load: ${e.target.src}`);
                                    e.target.src = 'fallback-image-url.jpg';
                                }}
                            />
                            <h3 className="category-title">{category.name}</h3>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CategoriesSection;
