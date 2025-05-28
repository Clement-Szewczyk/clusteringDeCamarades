// api.js
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000/';

const apiCluster = axios.create({
    baseURL: API_BASE_URL,
    timeout: 5000
});

apiCluster.interceptors.request.use(
    config => {
        const token = localStorage.getItem('authToken');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

export default apiCluster;