/**
 * Custom hooks for product data fetching with React Query
 */
import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { productApi } from '@/lib/api';
import type {
  ProductListResponse,
  ProductDetail,
  ProductStats,
  CategoryListResponse,
  BrandListResponse,
  ProductFilters,
} from '@/types/product';

/**
 * Hook to fetch paginated products list
 */
export function useProducts(filters: ProductFilters = {}) {
  return useQuery<ProductListResponse, Error>({
    queryKey: ['products', filters],
    queryFn: () => productApi.getProducts(filters),
    staleTime: 1000 * 60 * 2, // 2 minutes
    gcTime: 1000 * 60 * 5, // 5 minutes (previously cacheTime)
  });
}

/**
 * Hook to fetch single product
 */
export function useProduct(id: number): UseQueryResult<ProductDetail, Error> {
  return useQuery<ProductDetail, Error>({
    queryKey: ['product', id],
    queryFn: () => productApi.getProduct(id),
    enabled: !!id,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

/**
 * Hook to fetch product statistics
 */
export function useProductStats(): UseQueryResult<ProductStats, Error> {
  return useQuery<ProductStats, Error>({
    queryKey: ['productStats'],
    queryFn: () => productApi.getStats(),
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}

/**
 * Hook to fetch categories list
 */
export function useCategories(): UseQueryResult<CategoryListResponse, Error> {
  return useQuery<CategoryListResponse, Error>({
    queryKey: ['categories'],
    queryFn: () => productApi.getCategories(),
    staleTime: 1000 * 60 * 60, // 1 hour
  });
}

/**
 * Hook to fetch brands list
 */
export function useBrands(): UseQueryResult<BrandListResponse, Error> {
  return useQuery<BrandListResponse, Error>({
    queryKey: ['brands'],
    queryFn: () => productApi.getBrands(),
    staleTime: 1000 * 60 * 60, // 1 hour
  });
}
