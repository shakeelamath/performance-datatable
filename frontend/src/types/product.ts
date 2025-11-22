/**
 * Product data types
 */

export interface Product {
  id: number;
  sku: string;
  name: string;
  description: string | null;
  category: string;
  brand: string;
  price: string | number;
  stock_quantity: number;
  rating: string | number;
  reviews_count: number;
  created_at: string;
}

export interface ProductDetail extends Product {
  updated_at: string;
}

export interface ProductListResponse {
  data: Product[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export interface ProductStats {
  total_products: number;
  total_categories: number;
  total_brands: number;
  price_min: string | number;
  price_max: string | number;
  avg_rating: string | number;
  total_stock: number;
}

export interface CategoryListResponse {
  categories: string[];
  total: number;
}

export interface BrandListResponse {
  brands: string[];
  total: number;
}

export interface ProductFilters {
  page?: number;
  limit?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
  category?: string;
  brand?: string;
  min_price?: number;
  max_price?: number;
  search?: string;
}
