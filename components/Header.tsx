
import React from 'react';
import { Search, User, Heart, ShoppingBag, Menu } from 'lucide-react';

interface HeaderProps {
  cartCount: number;
}

const Header: React.FC<HeaderProps> = ({ cartCount }) => {
  return (
    <header className="sticky top-0 z-50 w-full">
      {/* Top Banner */}
      <div className="bg-[#333333] text-white py-2 text-center text-xs font-medium tracking-wide">
        FREE SHIPPING ON ORDERS OVER ₹999 | EASY 15-DAY RETURNS
      </div>

      {/* Main Header */}
      <div className="bg-white border-b border-gray-100 shadow-sm px-4 lg:px-8 py-3 lg:py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between gap-4 lg:gap-8">
          {/* Logo & Mobile Menu */}
          <div className="flex items-center gap-4">
            <button className="lg:hidden text-[#333333]">
              <Menu size={24} />
            </button>
            <div className="flex flex-col">
              <span className="text-xl lg:text-2xl font-bold tracking-tighter text-[#333333] italic">WALK n STYLE</span>
              <span className="text-[10px] tracking-[0.2em] font-medium text-gray-400 -mt-1 uppercase">Footwear for Every Step</span>
            </div>
          </div>

          {/* Search Bar */}
          <div className="hidden md:flex flex-1 max-w-xl relative">
            <input 
              type="text" 
              placeholder="Search for sandals, floaters, and more..." 
              className="w-full bg-gray-50 border border-gray-200 rounded-full py-2.5 px-6 pl-12 focus:outline-none focus:ring-2 focus:ring-black/5 focus:border-gray-400 transition-all text-sm"
            />
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
          </div>

          {/* Action Icons */}
          <div className="flex items-center gap-5 lg:gap-7">
            <button className="text-[#333333] hover:text-gray-600 transition-colors hidden sm:block">
              <User size={22} />
            </button>
            <button className="text-[#333333] hover:text-[#D32F2F] transition-colors relative">
              <Heart size={22} />
              <span className="absolute -top-1.5 -right-1.5 bg-[#D32F2F] text-white text-[10px] w-4 h-4 rounded-full flex items-center justify-center font-bold">0</span>
            </button>
            <button className="text-[#333333] hover:text-gray-600 transition-colors relative">
              <ShoppingBag size={22} />
              {cartCount > 0 && (
                <span className="absolute -top-1.5 -right-1.5 bg-black text-white text-[10px] w-4 h-4 rounded-full flex items-center justify-center font-bold">
                  {cartCount}
                </span>
              )}
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
