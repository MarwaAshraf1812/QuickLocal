import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import category1Image from '../assets/clothes.jpg'; // Replace with actual image paths
import category2Image from '../assets/home-food.jpg';
import category3Image from '../assets/kitchen.jpg';
import './Category.css'; // Ensure to create this CSS file for custom styles

const CategoriesSection = () => {
    return (
        <div className="container-fluid my-1 category-section">
            <div className="row justify-content-center align-items-center">
                <div className="col-md-3 mb-4">
                    <div className="category-card d-flex align-items-center">
                        <img src={category1Image} alt="Category 1" className="img-fluid category-image" />
                        <h3 className="category-title">Category 1</h3>
                    </div>
                </div>
                <div className="col-md-3 mb-4">
                    <div className="category-card d-flex align-items-center">
                        <img src={category2Image} alt="Category 2" className="img-fluid category-image" />
                        <h3 className="category-title text-center">Category 2</h3>
                    </div>
                </div>
                <div className="col-md-3 mb-4">
                    <div className="category-card d-flex align-items-center">
                        <img src={category3Image} alt="Category 3" className="img-fluid category-image" />
                        <h3 className="category-title">Category 3</h3>
                    </div>
                </div>
                <div className="col-md-3 mb-4">
                    <div className="category-card d-flex align-items-center">
                        <img src={category2Image} alt="Category 3" className="img-fluid category-image" />
                        <h3 className="category-title">Category 3</h3>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default CategoriesSection;
