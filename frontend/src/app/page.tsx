'use client';

import { DataTable } from '@/components/DataTable';

export default function HomePage() {
  return (
    <main className="container mx-auto py-10">
      <div className="mb-8">
        <h1 className="text-4xl font-bold tracking-tight">High Performance Data Table</h1>
        <p className="text-muted-foreground mt-2">
          Blazing fast virtual scrolling through 100,000+ product records
        </p>
      </div>
      
      <DataTable />
    </main>
  );
}
