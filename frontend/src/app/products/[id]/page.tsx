'use client';

import { useProduct } from '@/lib/hooks/useProducts';
import { formatPrice, formatRating, formatDate, formatNumber } from '@/lib/utils';
import {Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { ArrowLeft, Package, DollarSign, Star, Calendar, Hash } from 'lucide-react';
import Link from 'next/link';

export default function ProductDetailPage({ params }: { params: { id: string } }) {
  const productId = parseInt(params.id);
  const { data: product, isLoading, isError, error } = useProduct(productId);

  if (isLoading) {
    return (
      <main className="container mx-auto py-10">
        <Skeleton className="h-10 w-32 mb-6" />
        <Card>
          <CardHeader>
            <Skeleton className="h-8 w-3/4" />
            <Skeleton className="h-4 w-1/2 mt-2" />
          </CardHeader>
          <CardContent className="space-y-4">
            <Skeleton className="h-20 w-full" />
            <Skeleton className="h-20 w-full" />
            <Skeleton className="h-20 w-full" />
          </CardContent>
        </Card>
      </main>
    );
  }

  if (isError || !product) {
    return (
      <main className="container mx-auto py-10">
        <Link href="/">
          <Button variant="ghost">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Products
          </Button>
        </Link>
        <div className="rounded-lg border border-red-200 bg-red-50 p-8 text-center mt-6">
          <p className="text-red-800 font-medium">Product not found</p>
          <p className="text-red-600 text-sm mt-2">{error?.message}</p>
        </div>
      </main>
    );
  }

  return (
    <main className="container mx-auto py-10">
      <Link href="/">
        <Button variant="ghost" className="mb-6">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Products
        </Button>
      </Link>

      <div className="grid gap-6">
        {/* Main Product Card */}
        <Card>
          <CardHeader>
            <div className="flex items-start justify-between">
              <div className="space-y-2">
                <CardTitle className="text-3xl">{product.name}</CardTitle>
                <CardDescription className="flex items-center gap-2">
                  <Badge>{product.category}</Badge>
                  <span>•</span>
                  <span>{product.brand}</span>
                </CardDescription>
              </div>
              <div className="text-right">
                <div className="text-3xl font-bold text-primary">
                  {formatPrice(product.price)}
                </div>
                <div className="flex items-center gap-1 mt-1 text-sm">
                  <Star className="h-4 w-4 text-yellow-500 fill-yellow-500" />
                  <span className="font-medium">{formatRating(product.rating)}</span>
                  <span className="text-muted-foreground">
                    ({formatNumber(product.reviews_count)} reviews)
                  </span>
                </div>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Description */}
            {product.description && (
              <div>
                <h3 className="text-lg font-semibold mb-2">Description</h3>
                <p className="text-muted-foreground leading-relaxed">{product.description}</p>
              </div>
            )}

            {/* Product Details Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="rounded-lg border p-4">
                <div className="flex items-center gap-3">
                  <div className="rounded-full bg-primary/10 p-2">
                    <Hash className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">SKU</div>
                    <div className="font-mono font-medium">{product.sku}</div>
                  </div>
                </div>
              </div>

              <div className="rounded-lg border p-4">
                <div className="flex items-center gap-3">
                  <div className="rounded-full bg-primary/10 p-2">
                    <Package className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">Stock Quantity</div>
                    <div className={`font-medium ${product.stock_quantity < 50 ? 'text-red-600' : ''}`}>
                      {formatNumber(product.stock_quantity)} units
                    </div>
                  </div>
                </div>
              </div>

              <div className="rounded-lg border p-4">
                <div className="flex items-center gap-3">
                  <div className="rounded-full bg-primary/10 p-2">
                    <Calendar className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">Created Date</div>
                    <div className="font-medium">{formatDate(product.created_at)}</div>
                  </div>
                </div>
              </div>

              <div className="rounded-lg border p-4">
                <div className="flex items-center gap-3">
                  <div className="rounded-full bg-primary/10 p-2">
                    <Calendar className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <div className="text-sm text-muted-foreground">Last Updated</div>
                    <div className="font-medium">{formatDate(product.updated_at)}</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Product Stats */}
            <div className="rounded-lg bg-muted p-4">
              <h3 className="text-lg font-semibold mb-3">Product Information</h3>
              <dl className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div className="flex justify-between">
                  <dt className="text-muted-foreground">Product ID:</dt>
                  <dd className="font-medium">#{product.id}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-muted-foreground">Category:</dt>
                  <dd className="font-medium">{product.category}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-muted-foreground">Brand:</dt>
                  <dd className="font-medium">{product.brand}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-muted-foreground">Price:</dt>
                  <dd className="font-medium">{formatPrice(product.price)}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-muted-foreground">Rating:</dt>
                  <dd className="font-medium">{formatRating(product.rating)} ★</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-muted-foreground">Reviews:</dt>
                  <dd className="font-medium">{formatNumber(product.reviews_count)}</dd>
                </div>
              </dl>
            </div>
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
