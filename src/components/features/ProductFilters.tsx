import React, { useState } from 'react';
import { ChevronDown, ChevronUp, X } from 'lucide-react';
import { CATEGORIES, PRODUCTS } from '../../data/mockData';
import { Button } from '../ui/Button';

interface FilterState {
    categoryId: number | null;
    priceRange: [number, number];
    sizes: string[];
    colors: string[];
}

interface ProductFiltersProps {
    filters: FilterState;
    onFilterChange: (newFilters: FilterState) => void;
    onClearFilters: () => void;
}

export const ProductFilters: React.FC<ProductFiltersProps> = ({
    filters,
    onFilterChange,
    onClearFilters
}) => {
    const [openSections, setOpenSections] = useState<Record<string, boolean>>({
        category: true,
        price: true,
        size: true,
        color: true,
    });

    const toggleSection = (section: string) => {
        setOpenSections(prev => ({ ...prev, [section]: !prev[section] }));
    };

    // Derive available options from products (could be optimized)
    const allSizes = Array.from(new Set(PRODUCTS.flatMap(p => p.variants.map(v => v.size)))).sort();
    const allColors = Array.from(new Set(PRODUCTS.flatMap(p => p.variants.map(v => v.color)))).sort();

    // Helper to build category tree
    const renderCategoryTree = (parentId: number | null = null, depth = 0) => {
        const cats = CATEGORIES.filter(c => c.parent_id === parentId);
        if (cats.length === 0) return null;

        return (
            <ul className={`space-y-1 ${depth > 0 ? 'ml-4 border-l border-gray-100 pl-2' : ''}`}>
                {cats.map(cat => (
                    <li key={cat.id}>
                        <button
                            onClick={() => onFilterChange({ ...filters, categoryId: cat.id })}
                            className={`text-sm text-left hover:text-black transition-colors ${filters.categoryId === cat.id ? 'font-bold text-black' : 'text-gray-600'}`}
                        >
                            {cat.name}
                        </button>
                        {renderCategoryTree(cat.id, depth + 1)}
                    </li>
                ))}
            </ul>
        );
    };

    return (
        <div className="space-y-8">
            <div className="flex items-center justify-between">
                <h3 className="font-bold text-lg">Filters</h3>
                <button onClick={onClearFilters} className="text-xs text-gray-500 hover:text-black underline">
                    Clear All
                </button>
            </div>

            {/* Categories */}
            <div className="border-b border-gray-100 pb-6">
                <button
                    className="flex items-center justify-between w-full mb-4 font-bold"
                    onClick={() => toggleSection('category')}
                >
                    <span>Category</span>
                    {openSections.category ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                </button>
                {openSections.category && (
                    <div className="max-h-64 overflow-y-auto pr-2 scrollbar-thin">
                        {renderCategoryTree()}
                    </div>
                )}
            </div>

            {/* Price Range */}
            <div className="border-b border-gray-100 pb-6">
                <button
                    className="flex items-center justify-between w-full mb-4 font-bold"
                    onClick={() => toggleSection('price')}
                >
                    <span>Price</span>
                    {openSections.price ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                </button>
                {openSections.price && (
                    <div className="space-y-4">
                        <div className="flex items-center gap-4">
                            <div className="relative">
                                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 text-xs">₹</span>
                                <input
                                    type="number"
                                    value={filters.priceRange[0]}
                                    onChange={(e) => onFilterChange({ ...filters, priceRange: [Number(e.target.value), filters.priceRange[1]] })}
                                    className="w-full bg-gray-50 border border-gray-200 rounded px-3 py-2 pl-6 text-sm"
                                />
                            </div>
                            <span className="text-gray-400">-</span>
                            <div className="relative">
                                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 text-xs">₹</span>
                                <input
                                    type="number"
                                    value={filters.priceRange[1]}
                                    onChange={(e) => onFilterChange({ ...filters, priceRange: [filters.priceRange[0], Number(e.target.value)] })}
                                    className="w-full bg-gray-50 border border-gray-200 rounded px-3 py-2 pl-6 text-sm"
                                />
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Sizes */}
            <div className="border-b border-gray-100 pb-6">
                <button
                    className="flex items-center justify-between w-full mb-4 font-bold"
                    onClick={() => toggleSection('size')}
                >
                    <span>Size</span>
                    {openSections.size ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                </button>
                {openSections.size && (
                    <div className="flex flex-wrap gap-2">
                        {allSizes.map(size => (
                            <button
                                key={size}
                                onClick={() => {
                                    const newSizes = filters.sizes.includes(size)
                                        ? filters.sizes.filter(s => s !== size)
                                        : [...filters.sizes, size];
                                    onFilterChange({ ...filters, sizes: newSizes });
                                }}
                                className={`px-3 py-1 text-xs border rounded-md transition-all ${filters.sizes.includes(size)
                                        ? 'bg-black text-white border-black'
                                        : 'bg-white text-gray-600 border-gray-200 hover:border-black'
                                    }`}
                            >
                                {size}
                            </button>
                        ))}
                    </div>
                )}
            </div>

            {/* Colors */}
            <div className="pb-6">
                <button
                    className="flex items-center justify-between w-full mb-4 font-bold"
                    onClick={() => toggleSection('color')}
                >
                    <span>Color</span>
                    {openSections.color ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                </button>
                {openSections.color && (
                    <div className="space-y-2">
                        {allColors.map(color => (
                            <label key={color} className="flex items-center gap-3 cursor-pointer group">
                                <div className={`w-5 h-5 rounded-md border flex items-center justify-center transition-colors ${filters.colors.includes(color) ? 'bg-black border-black text-white' : 'bg-white border-gray-300 group-hover:border-black'}`}>
                                    {filters.colors.includes(color) && <X size={12} />}
                                </div>
                                <input
                                    type="checkbox"
                                    className="hidden"
                                    checked={filters.colors.includes(color)}
                                    onChange={() => {
                                        const newColors = filters.colors.includes(color)
                                            ? filters.colors.filter(c => c !== color)
                                            : [...filters.colors, color];
                                        onFilterChange({ ...filters, colors: newColors });
                                    }}
                                />
                                <span className="text-sm text-gray-600 group-hover:text-black">{color}</span>
                            </label>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};
