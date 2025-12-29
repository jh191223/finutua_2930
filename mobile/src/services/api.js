import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = 'https://your-domain.com/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

// 요청 인터셉터 (토큰 자동 추가)
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const authAPI = {
  register: (userData) => api.post('/users/register', userData),
  login: (email, password) => api.post('/users/login', { email, password }),
  getCurrentUser: () => api.get('/users/me'),
};

export const photoAPI = {
  upload: (formData) => api.post('/photos/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  list: () => api.get('/photos/list'),
};

export const avatarAPI = {
  generate: (photoId) => api.post('/avatars/generate', { photo_id: photoId }),
  get: (avatarId) => api.get(`/avatars/${avatarId}`),
};

export const logAPI = {
  addFood: (foodData) => api.post('/logs/food', foodData),
  addExercise: (exerciseData) => api.post('/logs/exercise', exerciseData),
  getDailyLogs: (date) => api.get(`/logs/daily?date=${date}`),
};

