
import React, { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { FilterState } from '../types';
import { GENDERS, SHOE_TYPES, SIZES, COLORS } from '../constants';

interface SidebarProps {
  filters: FilterState;
  onFilterChange: (category: keyof FilterState, value: any) => void;
  onClearFilters: () => void;
}

interface AccordionProps {
  title: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
}

const Accordion: React.FC<AccordionProps> = ({ title, children, defaultOpen = true }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="border-b border-gray-100 last:border-0 py-4">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center justify-between w-full text-left group"
      >
        <span className="text-sm font-semibold uppercase tracking-wider text-[#333333] group-hover:text-black transition-colors">
          {title}
        </span>
        {isOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
      </button>
      {isOpen && <div className="mt-4 animate-in fade-in slide-in-from-top-2 duration-300">{children}</div>}
    </div>
  );
};

const Sidebar: React.FC<SidebarProps> = ({ filters, onFilterChange, onClearFilters }) => {
  const handleCheckboxChange = (category: keyof FilterState, value: any) => {
    const currentValues = filters[category] as any[];
    const newValues = currentValues.includes(value)
      ? currentValues.filter(v => v !== value)
      : [...currentValues, value];
    onFilterChange(category, newValues);
  };

  return (
    <aside className="hidden lg:block w-full h-fit sticky top-32 overflow-y-auto max-h-[calc(100vh-140px)] pr-4 hide-scrollbar">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-bold text-[#333333]">Pick Your Look</h2>
        <button 
          onClick={onClearFilters}
          className="text-xs text-[#D32F2F] font-semibold hover:underline"
        >
          Clear All
        </button>
      </div>

      <Accordion title="Gender">
        <div className="space-y-2.5">
          {GENDERS.map((gender) => (
            <label key={gender} className="flex items-center gap-3 cursor-pointer group">
              <input 
                type="checkbox"
                checked={filters.gender.includes(gender)}
                onChange={() => handleCheckboxChange('gender', gender)}
                className="w-4 h-4 border-gray-300 rounded text-black focus:ring-black accent-black"
              />
              <span className="text-sm text-gray-600 group-hover:text-[#333333] transition-colors">{gender}</span>
            </label>
          ))}
        </div>
      </Accordion>

      <Accordion title="Shoe Type">
        <div className="space-y-2.5">
          {SHOE_TYPES.map((type) => (
            <label key={type} className="flex items-center gap-3 cursor-pointer group">
              <input 
                type="checkbox"
                checked={filters.type.includes(type)}
                onChange={() => handleCheckboxChange('type', type)}
                className="w-4 h-4 border-gray-300 rounded text-black focus:ring-black accent-black"
              />
              <span className="text-sm text-gray-600 group-hover:text-[#333333] transition-colors">{type}</span>
            </label>
          ))}
        </div>
      </Accordion>

      <Accordion title="Price">
        <div className="space-y-3">
          {[
            { label: 'Under ₹500', range: [0, 500] },
            { label: '₹500 - ₹800', range: [500, 800] },
            { label: 'Over ₹800', range: [800, 5000] },
          ].map((item) => (
            <label key={item.label} className="flex items-center gap-3 cursor-pointer group">
              <input 
                type="radio"
                name="price-range"
                checked={filters.priceRange[0] === item.range[0] && filters.priceRange[1] === item.range[1]}
                onChange={() => onFilterChange('priceRange', item.range)}
                className="w-4 h-4 border-gray-300 rounded-full text-black focus:ring-black accent-black"
              />
              <span className="text-sm text-gray-600 group-hover:text-[#333333] transition-colors">{item.label}</span>
            </label>
          ))}
        </div>
      </Accordion>

      <Accordion title="Size">
        <div className="grid grid-cols-4 gap-2">
          {SIZES.map((size) => (
            <button
              key={size}
              onClick={() => handleCheckboxChange('sizes', size)}
              className={`py-2 text-xs font-medium border transition-all ${
                filters.sizes.includes(size)
                  ? 'bg-black border-black text-white'
                  : 'bg-white border-gray-200 text-gray-600 hover:border-[#333333]'
              }`}
            >
              {size}
            </button>
          ))}
        </div>
      </Accordion>

      <Accordion title="Color">
        <div className="grid grid-cols-6 gap-3">
          {COLORS.map((color) => (
            <button
              key={color}
              title={color}
              onClick={() => handleCheckboxChange('colors', color)}
              className={`w-6 h-6 rounded-full border-2 transition-all p-0.5 ${
                filters.colors.includes(color) ? 'border-black' : 'border-transparent'
              }`}
            >
              <div 
                className={`w-full h-full rounded-full shadow-inner`}
                style={{ backgroundColor: color.toLowerCase() }}
              />
            </button>
          ))}
        </div>
      </Accordion>
    </aside>
  );
};

export default Sidebar;
