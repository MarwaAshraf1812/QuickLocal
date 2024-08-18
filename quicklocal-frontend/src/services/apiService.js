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
    getProductFilters: async (filter) => {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/products/?ordering=${filter}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    
}

export default apiService;