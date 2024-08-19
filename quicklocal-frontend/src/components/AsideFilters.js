import React, { useState } from 'react';

const AsideFilters = ({onFilterChange}) => {
    const [name, setName] = useState('');
    const [category, setCategory] = useState('');
    const [minPrice, setMinPrice] = useState('');
    const [maxPrice, setMaxPrice] = useState('');
    const [tags, setTags] = useState('');


    const handleFilterChange = () => {
        onFilterChange({
            name,
            category,
            minPrice,
            maxPrice,
            tags
        });
    };

    return(
        <aside className='col-md-9 'style={{ height: '100vh' }}>
            <div className='card mb-4 shadow-sm' style={{ height: '70%' }}>
                <div className='card-body'>
                    <h5 className="card-title blue-color fw-bold">Filters</h5>
                    <div className="mb-3">
                        <label htmlFor="nameFilter" className="form-label">Product name</label>
                        <input
                            type="text"
                            className="form-control"
                            id="nameFilter"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            onBlur={handleFilterChange}
                        />
                    </div>

                    <div className="mb-3">
                        <label htmlFor="categoryFilter" className="form-label">Category</label>
                        <input
                            type="text"
                            className="form-control"
                            id="categoryFilter"
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                            onBlur={handleFilterChange}
                        />
                    </div>

                    <div className="mb-3">
                        <label htmlFor="priceFilter" className="form-label">Price Range</label>
                        <div className="d-flex">
                            <input
                                type="number"
                                className="form-control me-2"
                                placeholder="Min"
                                value={minPrice}
                                onChange={(e) => setMinPrice(e.target.value)}
                                onBlur={handleFilterChange}
                            />
                            <input
                                type="number"
                                className="form-control"
                                placeholder="Max"
                                value={maxPrice}
                                onChange={(e) => setMaxPrice(e.target.value)}
                                onBlur={handleFilterChange}
                            />
                        </div>
                    </div>

                    <div className="mb-3">
                        <label htmlFor="tagsFilter" className="form-label">Tags</label>
                        <input
                            type="text"
                            className="form-control"
                            id="tagsFilter"
                            value={tags}
                            onChange={(e) => setTags(e.target.value)}
                            onBlur={handleFilterChange}
                        />
                    </div>
                </div>
            </div>
        </aside>
    );
};

export default AsideFilters;