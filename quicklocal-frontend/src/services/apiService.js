import axios from 'axios';


const apiService = {
    getCategories: async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/categories/');
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    getProducts: async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/products/')
            return response.data;
        } catch (error) {
            throw error;
        }

        
    },

    searchProducts: async (query) => {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/products/?search=${query}`)
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    sendMessage: async(message) => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/support/', message);
            return response.data;
        } catch (error) {
            throw error;
        }
    },

    getProductsByCategory: async (categoryId) => {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/category-products/?category=${categoryId}`)
            return response.data;
        } catch (error) {
            throw error;
        }
    },
    getProductFilters: async (filters = {}) => {
        const queryParams = new URLSearchParams();

        //Add filters
        if(filters.ordering) queryParams.append('ordering', filters.ordering);
        if (filters.category) queryParams.append('category', filters.category);
        if (filters.name) queryParams.append('name', filters.name);
        if (filters.min_price) queryParams.append('min_price', filters.min_price);
        if (filters.max_price) queryParams.append('max_price', filters.max_price);
        if (filters.rating) queryParams.append('rating', filters.rating);
        if (filters.tags && filters.tags.length > 0) {
            queryParams.append('tags', filters.tags.join(','));
        }
        try {
            const response = await axios.get(`http://127.0.0.1:8000/products/?${queryParams.toString()}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    
}

export default apiService;