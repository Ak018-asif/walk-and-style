export interface Category {
    id: number;
    name: string;
    parent_id: number | null;
}

export interface Product {
    id: number;
    category_id: number;
    name: string;
    description: string;
    base_price: number;
}

export interface ProductVariant {
    id: number;
    product_id: number;
    size: string;
    color: string;
    sku: string;
    stock_quantity: number;
}

export interface ProductImage {
    id: number;
    product_id: number;
    image_url: string;
    is_primary: boolean;
}

// Composite type for UI displays
export interface ProductWithDetails extends Product {
    images: ProductImage[];
    variants: ProductVariant[];
    category?: Category;
}
