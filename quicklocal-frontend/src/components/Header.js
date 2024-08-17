import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faShoppingCart, faHeart } from '@fortawesome/free-solid-svg-icons';
import './Header.css';
import { Link } from 'react-router-dom';
import apiService from '../services/apiService';

const Header = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResult, setSearchResult] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearchChange = async (e) => {
        const query = e.target.value;
        setSearchQuery(query);

        if (query.trim() === '') {
            setSearchResult([]);
            return;
        }

        setLoading(true);
        try {
            const results = await apiService.searchProducts(query);
            setSearchResult(results);
        } catch (err) {
            setError('Failed to fetch search results');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="header">
            <div className='container-fluid px-5 py-2 border sec-nav'>
                <div className="row align-items-center ">
                    <div className='col-md-2'>
                        <p className='logo'>QuickLocal</p>
                    </div>
                    <div className="col-md-8 d-flex justify-content-center">
                        <div className="input-group">
                            <input
                                type="text"
                                className="form-control border"
                                placeholder="Search for products..."
                                aria-label="Search for products..."
                                value={searchQuery}
                                onChange={handleSearchChange}
                            />
                            {loading && <div>Loading...</div>}
                            {error && <div>{error}</div>}
                            {searchResult.length > 0 && (
                                <div className="search-results">
                                    {searchResult.map(result => (
                                        <div key={result.id} className="search-result-item">
                                            <Link to={`/products/${result.id}`}>{result.name}</Link>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                    <div className="col-md-2 d-flex justify-content-end">
                        <div className='d-flex align-items-center'>
                            <FontAwesomeIcon icon={faUser} className='text-light fs-5 me-3 icon' />
                            <FontAwesomeIcon icon={faShoppingCart} className='text-light fs-5 me-3 icon' />
                            <FontAwesomeIcon icon={faHeart} className='text-light fs-5 icon' />
                        </div>
                    </div>
                </div>
            </div>
            <div className='container-fluid px-5 py-2 border main-nav'>
                <div className="row">
                    <div className='col'>
                        <ul className='nav justify-content-center'>
                            <li className='nav-item'>
                                <Link to='/' className='nav-link text-light'>Home</Link>
                            </li>
                            <li className='nav-item'>
                                <Link to='/Categories' className='nav-link text-light'>Categories</Link>
                            </li>
                            <li className='nav-item'>
                                <Link to='/shop' className='nav-link text-light'>Shop</Link>
                            </li>
                            <li className='nav-item'>
                                <Link to='/products' className='nav-link text-light'>Products</Link>
                            </li>
                            <li className='nav-item'>
                                <Link to='/contactUs' className='nav-link text-light'>Contact Us</Link>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Header;
