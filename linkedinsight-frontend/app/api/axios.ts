/**
 * Centralized Axios Instance for LinkedInsight API
 * 
 * Provides a configured Axios client with:
 * - Base URL from environment variables
 * - Request/response interceptors for logging
 * - Error handling
 * - Type-safe API calls
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';

// Get API URL from environment variable
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8001';

/**
 * Create Axios instance with default configuration
 */
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  timeout: 60000, // 60 seconds (AI endpoints can take longer)
});

/**
 * Request interceptor - logs outgoing requests
 */
apiClient.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    // Log request details in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`, {
        baseURL: config.baseURL,
        params: config.params,
        data: config.data,
      });
    }
    
    // Add any auth tokens here if needed in the future
    // const token = getAuthToken();
    // if (token) {
    //   config.headers = {
    //     ...config.headers,
    //     Authorization: `Bearer ${token}`,
    //   };
    // }
    
    return config;
  },
  (error: AxiosError) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

/**
 * Response interceptor - logs responses and handles errors
 */
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    // Log response details in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`[API Response] ${response.config.method?.toUpperCase()} ${response.config.url}`, {
        status: response.status,
        data: response.data,
      });
    }
    
    return response;
  },
  (error: AxiosError) => {
    // Enhanced error handling
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const data = error.response.data;
      
      console.error(`[API Error] ${error.config?.method?.toUpperCase()} ${error.config?.url}`, {
        status,
        data,
        message: error.message,
      });
      
      // Handle specific error codes
      switch (status) {
        case 401:
          console.error('Unauthorized - Authentication required');
          // Could redirect to login here
          break;
        case 403:
          console.error('Forbidden - Insufficient permissions');
          break;
        case 404:
          console.error('Not Found - Resource does not exist');
          break;
        case 500:
          console.error('Server Error - Internal server error');
          break;
        default:
          console.error(`HTTP Error ${status}`);
      }
    } else if (error.request) {
      // Request made but no response received
      const baseURL = error.config?.baseURL || API_BASE_URL;
      const fullURL = `${baseURL}${error.config?.url}`;
      
      console.error('[API Network Error]', {
        message: error.message,
        url: error.config?.url,
        baseURL: baseURL,
        fullURL: fullURL,
        code: error.code,
        request: error.request,
      });
      
      // Provide helpful error message
      if (error.code === 'ECONNREFUSED' || error.message.includes('ECONNREFUSED')) {
        console.error(`❌ Connection refused - Is the backend server running on ${baseURL}?`);
        console.error('   Make sure you started the FastAPI server with:');
        console.error(`   uvicorn app.main:app --host 127.0.0.1 --port 8001`);
      } else if (error.code === 'ETIMEDOUT' || error.message.includes('timeout')) {
        console.error('⏱️ Request timed out - The backend may be slow or unresponsive');
      } else {
        console.error(`❌ Network error - Could not connect to ${baseURL}`);
        console.error('   Check that:');
        console.error(`   1. Backend is running on ${baseURL}`);
        console.error('   2. Frontend .env.local has: NEXT_PUBLIC_API_URL=' + baseURL);
        console.error('   3. You restarted the frontend after changing .env.local');
      }
    } else {
      // Something else happened
      console.error('[API Error]', {
        message: error.message,
        config: error.config,
      });
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;

