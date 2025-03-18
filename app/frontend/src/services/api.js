import axios from 'axios';

const BASE_URL = 'http://localhost:8000/api';

const api = {
  search: (params) => {
    return axios.post(`${BASE_URL}/search`, params);
  },
  
  exportLeads: (leads) => {
    return axios.post(`${BASE_URL}/export`, { leads });
  },
  
  getConfig: () => {
    return axios.get(`${BASE_URL}/config`);
  },
  
  updateConfig: (config) => {
    return axios.post(`${BASE_URL}/config`, config);
  }
};

export default api; 