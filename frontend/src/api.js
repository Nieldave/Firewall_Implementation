import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

export const getLogs = () => axios.get(`${API_URL}/logs`);
export const getRules = () => axios.get(`${API_URL}/rules`);
export const addRule = (rule) => axios.post(`${API_URL}/rules`, rule);
export const updateRule = (rule) => axios.put(`${API_URL}/rules`, rule);
export const deleteRule = (id) => axios.delete(`${API_URL}/rules`, { data: { id } });