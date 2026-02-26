import React from 'react';
import { Heart, ShoppingBag } from 'lucide-react';
import { ProductWithDetails } from '../types';
import { Link } from 'react-router-dom';

interface ProductCardProps {
    product: ProductWithDetails;
    onAddToCart?: (product: ProductWithDetails) => void;
}

export const ProductCard: React.FC<ProductCardProps> = ({ product, onAddToCart }) => {
    const primaryImage = product.images.find(img => img.is_primary)?.image_url || product.images[0]?.image_url;

    // Get unique variants for display hints
    const colors = Array.from(new Set(product.variants.map(v => v.color)));

    return (
        <div className="group relative bg-white rounded-xl border border-gray-100 hover:shadow-xl transition-all duration-300 overflow-hidden">
            {/* Image Container */}
            <Link to={`/product/${product.id}`} className="block relative aspect-[4/5] bg-gray-50 overflow-hidden">
                <img
                    src={primaryImage}
                    alt={product.name}
                    className="w-full h-full object-cover object-center transition-transform duration-700 group-hover:scale-105"
                />
                {/* badges or tags can go here */}
                <button className="absolute top-3 right-3 p-2 bg-white/80 backdrop-blur-sm rounded-full text-gray-500 hover:text-red-500 hover:bg-white transition-colors opacity-0 group-hover:opacity-100 translate-x-2 group-hover:translate-x-0 duration-300">
                    <Heart size={18} />
                </button>
            </Link>

            {/* Info Container */}
            <div className="p-4">
                <div className="text-xs text-gray-400 mb-1">{colors.length} Colors</div>
                <Link to={`/product/${product.id}`}>
                    <h3 className="font-bold text-gray-900 mb-1 truncate hover:text-gray-600 transition-colors">{product.name}</h3>
                </Link>
                <p className="text-sm text-gray-500 line-clamp-2 mb-3 h-10">{product.description}</p>

                <div className="flex items-center justify-between mt-4">
                    <span className="text-lg font-bold">₹{product.base_price.toLocaleString()}</span>
                    <button
                        onClick={() => onAddToCart && onAddToCart(product)}
                        className="p-2 bg-black text-white rounded-full hover:bg-gray-800 transition-transform active:scale-95 transform translate-y-2 opacity-0 group-hover:translate-y-0 group-hover:opacity-100 duration-300"
                    >
                        <ShoppingBag size={18} />
                    </button>
                </div>
            </div>
        </div>
    );
};
