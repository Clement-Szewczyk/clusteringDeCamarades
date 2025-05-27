import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000/';

const apiCluster = axios.create({
    baseURL: API_BASE_URL,
    timeout: 5000,
    headers: {'Authorization': 'Bearer <token>'}
});

export default apiCluster;