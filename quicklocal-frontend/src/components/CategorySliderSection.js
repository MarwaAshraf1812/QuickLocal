import React, { useState, useEffect } from "react";
import Carousel from 'react-bootstrap/Carousel';
import './CategorySliderSection.css';
import apiService from '../services/apiService'; // Import your API service

const CategorySliderSection = () => {
    // States for categories, loading, and error
    const [categories, setCategories] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Fetching data from API
    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const data = await apiService.getCategories(); // Adjust according to your API method
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
    if (error) {
        return <p>{error}</p>;
    }

    return (
        <div className="container category-slider-section my-2">
            <div className="row">
                <div className="col-md-5 d-flex align-items-center">
                    <div className="data-column">
                        <h2>Shop By <span>Categories</span></h2>
                        <p>Explore our top categories of the season.</p>
                        <button className="explore-btn btn">Explore More</button>
                    </div>
                </div>
                <div className="col-md-7">
                    <Carousel>
                        {categories.map((category) => (
                            <Carousel.Item key={category.id}>
                                <div className="categorySlider-card d-flex align-items-center">
                                    <img
                                        src={category.image}
                                        alt={category.name}
                                        className="img-fluid categorySlider-image"
                                        onError={(e) => {
                                            console.error(`Image failed to load: ${e.target.src}`);
                                        }}
                                    />
                                </div>
                            </Carousel.Item>
                        ))}
                    </Carousel>
                </div>
            </div>
        </div>
    );
};

export default CategorySliderSection;
