import axios, { AxiosInstance } from 'axios';
import { User, Alert, DashboardKPIs, NotificationSettings } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

let authToken: string | null = null;

export const setAuthToken = (token: string | null) => {
  authToken = token;
};

const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  if (authToken) {
    config.headers.Authorization = `Bearer ${authToken}`;
  }
  return config;
});

// Auth API
export const login = async (email: string, password: string) => {
  const response = await apiClient.post('/api/auth/login', { email, password });
  return response.data;
};

export const register = async (
  email: string,
  username: string,
  password: string,
  first_name?: string,
  last_name?: string
) => {
  const response = await apiClient.post('/api/auth/register', {
    email,
    username,
    password,
    first_name,
    last_name,
  });
  return response.data;
};

export const getCurrentUser = async (): Promise<User> => {
  const response = await apiClient.get('/api/users/me');
  return response.data;
};

// Dashboard API
export const getDashboard = async () => {
  const response = await apiClient.get('/api/dashboard/');
  return response.data;
};

// Alerts API
export const getAlerts = async (page: number = 1, perPage: number = 20, filters?: any) => {
  const params = new URLSearchParams({
    page: page.toString(),
    per_page: perPage.toString(),
  });
  
  if (filters?.status) params.append('status', filters.status);
  if (filters?.severity) params.append('severity', filters.severity);
  
  const response = await apiClient.get(`/api/alerts/?${params.toString()}`);
  return response.data;
};

export const getAlert = async (alertId: string): Promise<Alert> => {
  const response = await apiClient.get(`/api/alerts/${alertId}`);
  return response.data;
};

export const updateAlert = async (alertId: string, updates: { status?: string }) => {
  const response = await apiClient.patch(`/api/alerts/${alertId}`, updates);
  return response.data;
};

export const getAlertStats = async () => {
  const response = await apiClient.get('/api/alerts/stats/summary');
  return response.data;
};

// Notifications API
export const getNotificationSettings = async (): Promise<NotificationSettings> => {
  const response = await apiClient.get('/api/notifications/settings');
  return response.data;
};

export const updateNotificationSettings = async (settings: Partial<NotificationSettings>) => {
  const response = await apiClient.patch('/api/notifications/settings', settings);
  return response.data;
};

// User API
export const updateProfile = async (updates: Partial<User>) => {
  const response = await apiClient.patch('/api/users/me', updates);
  return response.data;
};

export const changePassword = async (oldPassword: string, newPassword: string) => {
  const response = await apiClient.post('/api/users/me/change-password', {
    old_password: oldPassword,
    new_password: newPassword,
  });
  return response.data;
};

