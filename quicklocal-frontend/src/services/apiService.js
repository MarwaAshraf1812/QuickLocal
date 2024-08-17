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
    }
    
}

export default apiService;