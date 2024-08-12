import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import kitchenImage from '../assets/kitchen.jpg';
import clothesImage from '../assets/clothes.jpg';
import CategoriesSection from '../components/Category';
import './LandingPage.css';

const LandingPage = () => {
    return (
        <div className="container-fluid bg-light">
            <div className="row px-4">
                <div className="col-md-8 position-relative p-3">
                    <img
                        src={kitchenImage}
                        alt="Food"
                        className="img-fixed"
                    />
                    <div className="card overlay-card">
                        <div className="card-body">
                            <h2 className="card-title">Welcome to the <span>Quick Local</span></h2>
                            <p className="card-text">Grab Upto 50% off On Selected Kitchens Products</p>
                        </div>
                    </div>
                </div>
                <div className="col-md-4 d-flex align-items-center justify-content-center px-4">
                    <img
                        src={clothesImage}
                        alt="Clothes"
                        className="img-fixed"
                    />
                </div>
            </div>
            <div className="row category">
                <CategoriesSection />
            </div>
        </div>
    );
}

export default LandingPage;
