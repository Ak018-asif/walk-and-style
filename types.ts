
export interface Product {
  id: string;
  name: string;
  category: string;
  gender: 'Boy' | 'Girl' | 'Unisex';
  type: 'Sandal' | 'Floater' | 'Clog' | 'Flip-Flop';
  price: number;
  originalPrice: number;
  discount: number;
  rating: number;
  reviews: number;
  sizes: number[];
  colors: string[];
  imageUrl: string;
  isNew: boolean;
}

export interface FilterState {
  gender: string[];
  type: string[];
  priceRange: [number, number];
  sizes: number[];
  colors: string[];
}

export type SortOption = 'newest' | 'price-low-high' | 'price-high-low' | 'rating';
