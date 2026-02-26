
import React from 'react';
import { Star, Heart } from 'lucide-react';
import { Product } from '../types';

interface ProductCardProps {
  product: Product;
  onAddToCart: (id: string) => void;
}

const ProductCard: React.FC<ProductCardProps> = ({ product, onAddToCart }) => {
  return (
    <div className="group relative bg-white border border-gray-100 hover:shadow-xl transition-all duration-300 rounded-sm overflow-hidden flex flex-col h-full">
      {/* Badge Container */}
      <div className="absolute top-2 left-2 z-10 flex flex-col gap-1.5">
        {product.discount > 0 && (
          <span className="bg-[#D32F2F] text-white text-[10px] font-bold px-2 py-1 rounded-sm shadow-sm">
            -{product.discount}% OFF
          </span>
        )}
        {product.isNew && (
          <span className="bg-[#333333] text-white text-[10px] font-bold px-2 py-1 rounded-sm shadow-sm">
            NEW
          </span>
        )}
      </div>

      {/* Wishlist Button */}
      <button className="absolute top-3 right-3 z-10 p-1.5 bg-white/80 backdrop-blur-sm rounded-full opacity-0 group-hover:opacity-100 transition-opacity hover:bg-white hover:text-[#D32F2F]">
        <Heart size={18} />
      </button>

      {/* Image Section */}
      <div className="relative aspect-[4/5] overflow-hidden bg-gray-50">
        <img 
          src={product.imageUrl} 
          alt={product.name}
          className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
        />
        
        {/* Quick Add Overlay */}
        <div className="absolute bottom-0 left-0 w-full translate-y-full group-hover:translate-y-0 transition-transform duration-300 bg-black/90 px-4 py-3 flex items-center justify-between">
          <span className="text-white text-xs font-medium">Quick Add</span>
          <button 
            onClick={() => onAddToCart(product.id)}
            className="bg-white text-black text-[10px] font-bold py-1.5 px-3 rounded uppercase hover:bg-[#D32F2F] hover:text-white transition-colors"
          >
            Add to Bag
          </button>
        </div>
      </div>

      {/* Details Section */}
      <div className="p-4 flex flex-col flex-grow">
        <div className="flex items-center gap-1 mb-1.5">
          {[...Array(5)].map((_, i) => (
            <Star 
              key={i} 
              size={12} 
              className={i < Math.floor(product.rating) ? "fill-yellow-400 text-yellow-400" : "text-gray-200"}
            />
          ))}
          <span className="text-[10px] text-gray-400 ml-1">({product.reviews})</span>
        </div>

        <h3 className="text-sm font-medium text-[#333333] line-clamp-2 leading-tight mb-2 group-hover:text-black transition-colors min-h-[2.5rem]">
          {product.name}
        </h3>

        <div className="mt-auto pt-2 flex items-center gap-3">
          <span className="text-lg font-bold text-[#333333]">₹{product.price}</span>
          {product.originalPrice > product.price && (
            <span className="text-xs text-gray-400 line-through">₹{product.originalPrice}</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
