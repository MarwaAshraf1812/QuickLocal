import React from "react";
import './OffersSection.css';
import KitchenJPG from '../assets/kitchen.jpg';
import clothesJPG from '../assets/clothes.jpg';

const OffersSection = () => {
    return (
        <div className="offers container-fluid">
            <div className="row">
                <div className="col-md-6">
                    <div className="offers__card">
                        <img
                            src={KitchenJPG}
                            alt="Offer 1"
                            className="offers__card-image"
                        />
                        <div className="offers__card-overlay">
                            <div className="offers__card-title">Offer 1</div>
                            <div className="offers__card-description">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>
                        </div>
                    </div>
                </div>
                <div className="col-md-6">
                    <div className="offers__card">
                        <img
                            src={clothesJPG}
                            alt="Offer 2"
                            className="offers__card-image"
                        />
                        <div className="offers__card-overlay">
                            <div className="offers__card-title">Offer 2</div>
                            <div className="offers__card-description">Lorem ipsum dolor sit amet, consectetur adipiscing elit.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default OffersSection;
