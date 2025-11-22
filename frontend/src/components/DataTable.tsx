'use client';

import { useMemo, useState } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  ColumnDef,
  flexRender,
  SortingState,
} from '@tanstack/react-table';
import { useVirtualizer } from '@tanstack/react-virtual';
import { useProducts, useProductStats, useCategories, useBrands } from '@/lib/hooks/useProducts';
import { useDebounce } from '@/lib/hooks/useDebounce';
import { Product } from '@/types/product';
import { formatPrice, formatNumber, formatRating } from '@/lib/utils';
import { TableFilters } from '@/components/TableFilters';
import { TablePagination } from '@/components/TablePagination';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { ArrowUpDown, Eye } from 'lucide-react';
import Link from 'next/link';
import { useRef } from 'react';

export function DataTable() {
  const [page, setPage] = useState(1);
  const [limit] = useState(50);
  const [sorting, setSorting] = useState<SortingState>([]);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [brand, setBrand] = useState('');
  const [priceRange, setPriceRange] = useState<[number, number]>([0, 10000]);

  const debouncedSearch = useDebounce(search, 300);

  const sortBy = sorting[0]?.id || 'id';
  const sortOrder = sorting[0]?.desc ? 'desc' : 'asc';

  const { data, isLoading, isError, error } = useProducts({
    page,
    limit,
    sort_by: sortBy,
    sort_order: sortOrder,
    search: debouncedSearch,
    category: category || undefined,
    brand: brand || undefined,
    min_price: priceRange[0] || undefined,
    max_price: priceRange[1] !== 10000 ? priceRange[1] : undefined,
  });

  const { data: stats } = useProductStats();
  const { data: categories } = useCategories();
  const { data: brands } = useBrands();

  const columns = useMemo<ColumnDef<Product>[]>(
    () => [
      {
        accessorKey: 'id',
        header: ({ column }) => {
          return (
            <Button
              variant="ghost"
              onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
            >
              ID
              <ArrowUpDown className="ml-2 h-4 w-4" />
            </Button>
          );
        },
        cell: ({ row }) => <div className="font-medium">{row.original.id}</div>,
        size: 80,
      },
      {
        accessorKey: 'sku',
        header: 'SKU',
        cell: ({ row }) => <div className="font-mono text-sm">{row.original.sku}</div>,
        size: 150,
      },
      {
        accessorKey: 'name',
        header: ({ column }) => {
          return (
            <Button
              variant="ghost"
              onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
            >
              Name
              <ArrowUpDown className="ml-2 h-4 w-4" />
            </Button>
          );
        },
        cell: ({ row }) => (
          <div className="max-w-[300px] truncate font-medium">{row.original.name}</div>
        ),
        size: 300,
      },
      {
        accessorKey: 'category',
        header: ({ column }) => {
          return (
            <Button
              variant="ghost"
              onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
            >
              Category
              <ArrowUpDown className="ml-2 h-4 w-4" />
            </Button>
          );
        },
        cell: ({ row }) => <Badge variant="secondary">{row.original.category}</Badge>,
        size: 150,
      },
      {
        accessorKey: 'brand',
        header: ({ column }) => {
          return (
            <Button
              variant="ghost"
              onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
            >
              Brand
              <ArrowUpDown className="ml-2 h-4 w-4" />
            </Button>
          );
        },
        cell: ({ row }) => <div>{row.original.brand}</div>,
        size: 120,
      },
      {
        accessorKey: 'price',
        header: ({ column }) => {
          return (
            <Button
              variant="ghost"
              onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
            >
              Price
              <ArrowUpDown className="ml-2 h-4 w-4" />
            </Button>
          );
        },
        cell: ({ row }) => (
          <div className="font-semibold">{formatPrice(row.original.price)}</div>
        ),
        size: 120,
      },
      {
        accessorKey: 'stock_quantity',
        header: 'Stock',
        cell: ({ row }) => {
          const stock = row.original.stock_quantity;
          return (
            <div className={stock < 50 ? 'text-red-600 font-medium' : ''}>
              {formatNumber(stock)}
            </div>
          );
        },
        size: 100,
      },
      {
        accessorKey: 'rating',
        header: ({ column }) => {
          return (
            <Button
              variant="ghost"
              onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
            >
              Rating
              <ArrowUpDown className="ml-2 h-4 w-4" />
            </Button>
          );
        },
        cell: ({ row }) => (
          <div className="flex items-center gap-1">
            <span className="text-yellow-500">★</span>
            <span>{formatRating(row.original.rating)}</span>
            <span className="text-muted-foreground text-xs">
              ({formatNumber(row.original.reviews_count)})
            </span>
          </div>
        ),
        size: 150,
      },
      {
        id: 'actions',
        header: 'Actions',
        cell: ({ row }) => (
          <Link href={`/products/${row.original.id}`}>
            <Button variant="ghost" size="sm">
              <Eye className="h-4 w-4 mr-1" />
              View
            </Button>
          </Link>
        ),
        size: 100,
      },
    ],
    []
  );

  const table = useReactTable({
    data: data?.data || [],
    columns,
    state: {
      sorting,
    },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    manualSorting: true,
    manualPagination: true,
  });

  const tableContainerRef = useRef<HTMLDivElement>(null);

  const { rows } = table.getRowModel();

  const rowVirtualizer = useVirtualizer({
    count: rows.length,
    getScrollElement: () => tableContainerRef.current,
    estimateSize: () => 60,
    overscan: 10,
  });

  if (isError) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-8 text-center">
        <p className="text-red-800 font-medium">Error loading products</p>
        <p className="text-red-600 text-sm mt-2">{error?.message}</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Stats Bar */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="rounded-lg border bg-card p-4">
            <div className="text-sm text-muted-foreground">Total Products</div>
            <div className="text-2xl font-bold">{formatNumber(stats.total_products)}</div>
          </div>
          <div className="rounded-lg border bg-card p-4">
            <div className="text-sm text-muted-foreground">Categories</div>
            <div className="text-2xl font-bold">{stats.total_categories}</div>
          </div>
          <div className="rounded-lg border bg-card p-4">
            <div className="text-sm text-muted-foreground">Price Range</div>
            <div className="text-2xl font-bold">
              {formatPrice(stats.price_min)} - {formatPrice(stats.price_max)}
            </div>
          </div>
          <div className="rounded-lg border bg-card p-4">
            <div className="text-sm text-muted-foreground">Avg Rating</div>
            <div className="text-2xl font-bold">★ {formatRating(stats.avg_rating)}</div>
          </div>
        </div>
      )}

      {/* Filters */}
      <TableFilters
        search={search}
        onSearchChange={setSearch}
        category={category}
        onCategoryChange={setCategory}
        brand={brand}
        onBrandChange={setBrand}
        priceRange={priceRange}
        onPriceRangeChange={setPriceRange}
        categories={categories?.categories || []}
        brands={brands?.brands || []}
      />

      {/* Table */}
      <div className="rounded-lg border bg-card">
        <div
          ref={tableContainerRef}
          className="relative h-[600px] overflow-auto"
          style={{ contain: 'strict' }}
        >
          {isLoading ? (
            <div className="p-8 space-y-4">
              {Array.from({ length: 10 }).map((_, i) => (
                <Skeleton key={i} className="h-12 w-full" />
              ))}
            </div>
          ) : (
            <table className="w-full border-collapse">
              <thead className="sticky top-0 z-10 bg-muted/95 backdrop-blur">
                {table.getHeaderGroups().map((headerGroup) => (
                  <tr key={headerGroup.id} className="border-b">
                    {headerGroup.headers.map((header) => (
                      <th
                        key={header.id}
                        className="h-12 px-4 text-left align-middle font-medium"
                        style={{ width: header.getSize() }}
                      >
                        {header.isPlaceholder
                          ? null
                          : flexRender(header.column.columnDef.header, header.getContext())}
                      </th>
                    ))}
                  </tr>
                ))}
              </thead>
              <tbody style={{ height: `${rowVirtualizer.getTotalSize()}px` }}>
                {rowVirtualizer.getVirtualItems().map((virtualRow) => {
                  const row = rows[virtualRow.index];
                  return (
                    <tr
                      key={row.id}
                      className="border-b hover:bg-muted/50 transition-colors"
                      style={{
                        position: 'absolute',
                        transform: `translateY(${virtualRow.start}px)`,
                        width: '100%',
                      }}
                    >
                      {row.getVisibleCells().map((cell) => (
                        <td
                          key={cell.id}
                          className="p-4 align-middle"
                          style={{ width: cell.column.getSize() }}
                        >
                          {flexRender(cell.column.columnDef.cell, cell.getContext())}
                        </td>
                      ))}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Pagination */}
      {data && (
        <TablePagination
          page={page}
          totalPages={data.pages}
          total={data.total}
          limit={limit}
          onPageChange={setPage}
        />
      )}
    </div>
  );
}
