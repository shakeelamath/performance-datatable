/**
 * API client for backend communication
 */
import axios from 'axios';
import type {
  Product,
  ProductDetail,
  ProductListResponse,
  ProductStats,
  CategoryListResponse,
  BrandListResponse,
  ProductFilters,
} from '@/types/product';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_PREFIX = '/api/v1';

// Create axios instance
const apiClient = axios.create({
  baseURL: `${API_BASE_URL}${API_PREFIX}`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add any auth tokens or custom headers here
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle errors globally
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

/**
 * Product API methods
 */
export const productApi = {
  /**
   * Get paginated list of products with filters
   */
  getProducts: async (filters: ProductFilters = {}): Promise<ProductListResponse> => {
    const params = new URLSearchParams();
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params.append(key, String(value));
      }
    });
    
    const response = await apiClient.get<ProductListResponse>(`/products?${params.toString()}`);
    return response.data;
  },

  /**
   * Get single product by ID
   */
  getProduct: async (id: number): Promise<ProductDetail> => {
    const response = await apiClient.get<ProductDetail>(`/products/${id}`);
    return response.data;
  },

  /**
   * Get product statistics
   */
  getStats: async (): Promise<ProductStats> => {
    const response = await apiClient.get<ProductStats>('/products/stats');
    return response.data;
  },

  /**
   * Get list of categories
   */
  getCategories: async (): Promise<CategoryListResponse> => {
    const response = await apiClient.get<CategoryListResponse>('/products/categories');
    return response.data;
  },

  /**
   * Get list of brands
   */
  getBrands: async (): Promise<BrandListResponse> => {
    const response = await apiClient.get<BrandListResponse>('/products/brands');
    return response.data;
  },
};

export default apiClient;
