# Frontend - High-Performance Data Table

Next.js 14 frontend with TanStack Table, virtual scrolling, and real-time filtering.

## Features

- ✅ Virtual scrolling for smooth performance with 100k+ records
- ✅ Real-time search with debouncing
- ✅ Multi-column filtering (category, brand, price range)
- ✅ Sortable columns
- ✅ Pagination
- ✅ Product detail page
- ✅ Responsive design
- ✅ Loading states and error handling
- ✅ shadcn/ui components

## Tech Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **TanStack Table v8** - Headless table library
- **TanStack Virtual** - Virtual scrolling
- **TanStack Query (React Query)** - Data fetching & caching
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI components
- **Axios** - HTTP client
- **Lucide React** - Icons

## Getting Started

### Prerequisites
- Node.js 18+ or npm/yarn
- Backend API running on http://localhost:8000

### Installation

```bash
# Install dependencies
npm install

# or
yarn install
```

### Development

```bash
# Run development server
npm run dev

# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
# Build the application
npm run build

# Start production server
npm start
```

### Docker

```bash
# Build Docker image
docker build -t frontend-app .

# Run container
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:8000 frontend-app
```

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Root layout
│   │   ├── page.tsx             # Home page with data table
│   │   ├── providers.tsx        # React Query provider
│   │   ├── globals.css          # Global styles
│   │   └── products/
│   │       └── [id]/
│   │           └── page.tsx     # Product detail page
│   ├── components/
│   │   ├── ui/                  # shadcn/ui components
│   │   ├── DataTable.tsx        # Main data table with virtual scrolling
│   │   ├── TableFilters.tsx    # Filter controls
│   │   └── TablePagination.tsx # Pagination component
│   ├── lib/
│   │   ├── api.ts              # API client
│   │   ├── utils.ts            # Utility functions
│   │   └── hooks/
│   │       ├── useProducts.ts  # React Query hooks
│   │       └── useDebounce.ts  # Debounce hook
│   └── types/
│       └── product.ts          # TypeScript interfaces
├── public/
├── Dockerfile
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

## Key Components

### DataTable
Main data table component with:
- Virtual scrolling using TanStack Virtual
- Sorting via TanStack Table
- Filters and search
- Pagination
- Loading states

### TableFilters
Filter controls for:
- Search input (debounced 300ms)
- Category dropdown
- Brand dropdown
- Price range inputs
- Clear all button

### TablePagination
Pagination component with:
- First/Previous/Next/Last buttons
- Current page indicator
- Total items count

### Product Detail Page
Dynamic route showing:
- Full product information
- Price and ratings
- Stock quantity
- Created/updated dates
- Back button to table

## Performance Optimizations

### Virtual Scrolling
- Only renders visible rows (~10-15 rows at a time)
- Smooth scrolling through 100k+ records
- Configurable overscan for smooth UX

### Data Caching
- React Query caches API responses
- Stale time: 2 minutes for lists, 5 minutes for details
- Background refetching disabled
- Automatic retry on failure

### Debouncing
- Search input debounced by 300ms
- Prevents excessive API calls
- Better UX and reduced server load

### Code Splitting
- Dynamic imports for detail page
- Smaller initial bundle
- Faster page loads

### Memoization
- Column definitions memoized
- Prevents unnecessary re-renders
- Better React performance

## Environment Variables

Create `.env.local` file:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Integration

The frontend connects to the backend API:

```typescript
// List products with filters
GET /api/v1/products?page=1&limit=50&category=Electronics

// Get product detail
GET /api/v1/products/123

// Get statistics
GET /api/v1/products/stats

// Get categories
GET /api/v1/products/categories

// Get brands
GET /api/v1/products/brands
```

## Responsive Design

- **Mobile**: Single column, stacked filters
- **Tablet**: Two-column filters
- **Desktop**: Four-column filters, full table

All components are fully responsive using Tailwind CSS breakpoints.

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)

## Performance Targets

- ✅ Initial page load: < 2 seconds
- ✅ Time to Interactive: < 3 seconds
- ✅ First Contentful Paint: < 1 second
- ✅ Smooth 60fps scrolling
- ✅ Instant search feedback (< 300ms)

## Troubleshooting

**Issue: "Cannot connect to API"**
- Ensure backend is running on http://localhost:8000
- Check NEXT_PUBLIC_API_URL environment variable
- Verify CORS settings in backend

**Issue: "Virtual scrolling stutters"**
- Check browser performance
- Reduce overscan value in DataTable.tsx
- Ensure adequate system resources

**Issue: "Styles not loading"**
- Run `npm run dev` to rebuild
- Clear .next cache: `rm -rf .next`
- Check Tailwind config

## Contributing

1. Install dependencies: `npm install`
2. Run dev server: `npm run dev`
3. Make changes
4. Test thoroughly
5. Build for production: `npm run build`

## License

MIT
