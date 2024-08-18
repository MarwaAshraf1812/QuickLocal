import React from 'react';
import './Footer.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFacebook, faTwitter, faInstagram } from '@fortawesome/free-brands-svg-icons';

const Footer = () => {
    return (
        <footer className="footer py-2">
            <div className="container">
                <div className="row">
                    <div className="col-md-3 ">
                        <h4 className="footer-logo">QuickLocal</h4>
                        <p>Your go-to place for local shopping.</p>
                    </div>
                    
                    <div className="col-md-3 ">
                        <h5>Quick Links</h5>
                        <ul className="list-unstyled">
                            <li><a href="/" className='custom-color'>Home</a></li>
                            <li><a href="/categories" className='custom-color'>Categories</a></li>
                            <li><a href="/shop" className='custom-color'>Shop</a></li>
                            <li><a href="/contactUs" className='custom-color'>Contact Us</a></li>
                        </ul>
                    </div>

                    <div className="col-md-3 ">
                        <h5>Support</h5>
                        <ul className="list-unstyled">
                            <li><a href="/faq" className='custom-color'>FAQ</a></li>
                            <li><a href="/shipping" className='custom-color'>Shipping Information</a></li>
                            <li><a href="/returns" className='custom-color'>Returns</a></li>
                            <li><a href="/support" className='custom-color'>Customer Support</a></li>
                        </ul>
                    </div>

                    <div className="col-md-3">
                        <h5>Follow Us</h5>
                        <ul className="list-unstyled d-flex">
                            <li><a href="https://facebook.com" className="me-3 custom-color"><FontAwesomeIcon icon={faFacebook} size="2x" /></a></li>
                            <li><a href="https://twitter.com" className="me-3 custom-color"><FontAwesomeIcon icon={faTwitter} size="2x" /></a></li>
                            <li><a href="https://instagram.com"><FontAwesomeIcon className="custom-color" icon={faInstagram} size="2x" /></a></li>
                        </ul>
                    </div>
                </div>

                <hr />
                <div className="text-center">
                    <p>&copy; 2024 QuickLocal. All Rights Reserved.</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
