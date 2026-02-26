
import React, { useState, useEffect, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Navbar } from '../components/layout/Navbar';
import { Footer } from '../components/layout/Footer';
import { ProductFilters } from '../components/features/ProductFilters';
import { ProductCard } from '../components/ProductCard';
import { CATEGORIES } from '../data/mockData';
import { SlidersHorizontal } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { api } from '../api';
import { ProductWithDetails } from '../types';

export const ProductListing: React.FC = () => {
    const [searchParams] = useSearchParams();
    const initialCategoryId = searchParams.get('category');

    const [isMobileFiltersOpen, setIsMobileFiltersOpen] = useState(false);
    const [filters, setFilters] = useState({
        categoryId: initialCategoryId ? Number(initialCategoryId) : null,
        priceRange: [0, 10000] as [number, number],
        sizes: [] as string[],
        colors: [] as string[],
    });

    const [products, setProducts] = useState<ProductWithDetails[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    // Sync with URL params if they change
    useEffect(() => {
        const catId = searchParams.get('category');
        if (catId) {
            setFilters(prev => ({ ...prev, categoryId: Number(catId) }));
        }
    }, [searchParams]);

    // Fetch products when filters change
    useEffect(() => {
        const fetchProducts = async () => {
            setIsLoading(true);
            try {
                const params: any = {};
                if (filters.categoryId) params.category_id = filters.categoryId;
                if (filters.priceRange[0] > 0) params.min_price = filters.priceRange[0];
                if (filters.priceRange[1] < 10000) params.max_price = filters.priceRange[1];
                // backend doesn't support size/color filtering yet in this iteration, 
                // but we can client-side filter or ignore for now as per plan focus on DB integration

                const data = await api.getProducts(params);

                // Client-side filtering for size/color if needed (since backend logic was minimal for those)
                let result = data;
                if (filters.sizes.length > 0) {
                    result = result.filter((p: ProductWithDetails) => p.variants.some(v => filters.sizes.includes(v.size)));
                }
                if (filters.colors.length > 0) {
                    result = result.filter((p: ProductWithDetails) => p.variants.some(v => filters.colors.includes(v.color)));
                }

                setProducts(result);
            } catch (error) {
                console.error("Failed to fetch products", error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchProducts();
    }, [filters]);

    const activeCategoryName = "Products"; // We could fetch category name by ID if needed

    return (
        <div className="min-h-screen bg-white">
            <Navbar />

            <main className="pt-20 pb-12 max-w-7xl mx-auto px-4 lg:px-8">
                {/* Header */}
                <div className="py-8 border-b border-gray-100 flex flex-col sm:flex-row justify-between items-end gap-4">
                    <div>
                        <div className="text-sm text-gray-500 mb-2">Home / Products</div>
                        <h1 className="text-3xl font-black italic tracking-tight">{activeCategoryName}</h1>
                        <p className="text-gray-500 mt-2">{products.length} items found</p>
                    </div>

                    <Button
                        variant="outline"
                        className="lg:hidden gap-2"
                        onClick={() => setIsMobileFiltersOpen(true)}
                    >
                        <SlidersHorizontal size={18} /> Filters
                    </Button>
                </div>

                <div className="flex gap-8 mt-8">
                    {/* Sidebar (Desktop) */}
                    <aside className="hidden lg:block w-64 shrink-0">
                        <ProductFilters
                            filters={filters}
                            onFilterChange={setFilters}
                            onClearFilters={() => setFilters({
                                categoryId: null,
                                priceRange: [0, 10000],
                                sizes: [],
                                colors: [],
                            })}
                        />
                    </aside>

                    {/* Product Grid */}
                    <div className="flex-1">
                        {isLoading ? (
                            <div className="text-center py-20">Loading...</div>
                        ) : products.length > 0 ? (
                            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6">
                                {products.map(product => (
                                    <ProductCard key={product.id} product={product} />
                                ))}
                            </div>
                        ) : (
                            <div className="text-center py-20 bg-gray-50 rounded-xl">
                                <h3 className="text-xl font-bold mb-2">No products found</h3>
                                <p className="text-gray-500">Try adjusting your filters.</p>
                            </div>
                        )}
                    </div>
                </div>
            </main>

            {/* Mobile Filters Overlay */}
            {isMobileFiltersOpen && (
                <div className="fixed inset-0 z-50 bg-black/50 lg:hidden flex justify-end">
                    <div className="w-80 bg-white h-full overflow-y-auto p-6 animate-in slide-in-from-right">
                        <div className="flex justify-between items-center mb-6">
                            <h2 className="text-xl font-bold">Filters</h2>
                            <Button variant="ghost" size="sm" onClick={() => setIsMobileFiltersOpen(false)}>Close</Button>
                        </div>
                        <ProductFilters
                            filters={filters}
                            onFilterChange={setFilters}
                            onClearFilters={() => {
                                setFilters({
                                    categoryId: null,
                                    priceRange: [0, 10000],
                                    sizes: [],
                                    colors: [],
                                });
                                setIsMobileFiltersOpen(false);
                            }}
                        />
                        <div className="mt-8 pt-4 border-t border-gray-100">
                            <Button className="w-full" onClick={() => setIsMobileFiltersOpen(false)}>Show Results</Button>
                        </div>
                    </div>
                </div>
            )}

            <Footer />
        </div>
    );
};
