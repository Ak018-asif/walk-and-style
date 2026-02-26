import { Category, Product, ProductWithDetails, ProductVariant, ProductImage } from '../types';

export const CATEGORIES: Category[] = [
    // Men
    { id: 1, name: 'Men', parent_id: null },
    { id: 2, name: 'Shoes', parent_id: 1 },
    { id: 3, name: 'Formal', parent_id: 2 },
    { id: 4, name: 'Casual', parent_id: 2 },
    { id: 5, name: 'Sandals', parent_id: 1 },
    { id: 6, name: 'Hawais', parent_id: 1 },
    { id: 7, name: 'Perfumes', parent_id: 1 },
    { id: 8, name: 'Belts', parent_id: 1 },
    { id: 9, name: 'Autolock', parent_id: 8 },
    { id: 10, name: 'Casual belt', parent_id: 8 },

    // Women
    { id: 11, name: 'Women', parent_id: null },
    { id: 12, name: 'Shoes', parent_id: 11 },
    { id: 13, name: 'Sandals', parent_id: 11 },
    { id: 14, name: 'Perfumes', parent_id: 11 },
    { id: 15, name: 'Casual (v-shape)', parent_id: 11 },

    // Kids
    { id: 16, name: 'Kids', parent_id: null },
    { id: 17, name: 'Boys & Girls', parent_id: 16 },
    { id: 18, name: 'Shoes (casual)', parent_id: 16 },
    { id: 19, name: 'Sandals', parent_id: 16 },
    { id: 20, name: 'Hawai and crocs', parent_id: 16 },

    // Accessories
    { id: 21, name: 'Accessories', parent_id: null },
    { id: 22, name: 'Bags', parent_id: 21 },
    { id: 23, name: 'Gym bags', parent_id: 22 },
    { id: 24, name: 'School and college bags', parent_id: 22 },
    { id: 25, name: 'Tourister bags', parent_id: 22 },
    { id: 26, name: 'Extras', parent_id: 21 },
    { id: 27, name: 'Shoe polish and socks', parent_id: 26 },
];

export const PRODUCTS: ProductWithDetails[] = [
    // Men's Casual Shoe
    {
        id: 101,
        category_id: 4, // Men > Shoes > Casual
        name: 'Urban Trekker Sneakers',
        description: 'Lightweight and breathable casual sneakers perfect for daily wear. Features a cushioned sole for all-day comfort.',
        base_price: 2499,
        images: [
            { id: 1, product_id: 101, image_url: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&q=80&w=1000', is_primary: true },
            { id: 2, product_id: 101, image_url: 'https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?auto=format&fit=crop&q=80&w=1000', is_primary: false },
        ],
        variants: [
            { id: 1, product_id: 101, size: '40', color: 'Red/White', sku: 'UTS-RD-40', stock_quantity: 10 },
            { id: 2, product_id: 101, size: '41', color: 'Red/White', sku: 'UTS-RD-41', stock_quantity: 5 },
            { id: 3, product_id: 101, size: '42', color: 'Red/White', sku: 'UTS-RD-42', stock_quantity: 0 },
            { id: 4, product_id: 101, size: '40', color: 'Black/White', sku: 'UTS-BK-40', stock_quantity: 8 },
        ],
    },
    // Men's Formal Shoe
    {
        id: 102,
        category_id: 3, // Men > Shoes > Formal
        name: 'Classic Oxford Leather',
        description: 'Premium genuine leather Oxford shoes. Elegant design suitable for business and formal occasions.',
        base_price: 3999,
        images: [
            { id: 3, product_id: 102, image_url: 'https://images.unsplash.com/photo-1614252369475-531eba835eb1?auto=format&fit=crop&q=80&w=1000', is_primary: true },
        ],
        variants: [
            { id: 5, product_id: 102, size: '40', color: 'Brown', sku: 'COL-BR-40', stock_quantity: 12 },
            { id: 6, product_id: 102, size: '41', color: 'Black', sku: 'COL-BK-41', stock_quantity: 7 },
        ],
    },
    // Women's Sandals
    {
        id: 201,
        category_id: 13, // Women > Sandals
        name: 'Summer Breeze Strappy Sandals',
        description: 'Chic and comfortable strappy sandals, perfect for summer outings. Features a soft footbed.',
        base_price: 1299,
        images: [
            { id: 4, product_id: 201, image_url: 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&q=80&w=1000', is_primary: true },
        ],
        variants: [
            { id: 7, product_id: 201, size: '36', color: 'Gold', sku: 'SBS-GD-36', stock_quantity: 20 },
            { id: 8, product_id: 201, size: '37', color: 'Silver', sku: 'SBS-SL-37', stock_quantity: 15 },
        ],
    },
    // Kids' Shoes
    {
        id: 301,
        category_id: 18, // Kids > Shoes (casual)
        name: 'Dino Stomp Light-Up Shoes',
        description: 'Fun and durable shoes with light-up soles. Kids will love the dinosaur theme.',
        base_price: 899,
        images: [
            { id: 5, product_id: 301, image_url: 'https://images.unsplash.com/photo-1514989940723-e887532d5588?auto=format&fit=crop&q=80&w=1000', is_primary: true },
        ],
        variants: [
            { id: 9, product_id: 301, size: '28', color: 'Green', sku: 'DSL-GR-28', stock_quantity: 30 },
            { id: 10, product_id: 301, size: '30', color: 'Blue', sku: 'DSL-BL-30', stock_quantity: 25 },
        ],
    },
    // Kids' Sandals
    {
        id: 302,
        category_id: 19, // Kids > Sandals
        name: 'Rainbow Straps',
        description: 'Colorful sandals with adjustable velcro straps. Easy for kids to put on and take off.',
        base_price: 599,
        images: [
            { id: 6, product_id: 302, image_url: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRzZ7jZ7jZ7jZ7jZ7jZ7jZ7jZ7jZ7jZ7jZ7jZ&s', is_primary: true }, // Placeholder or meaningful URL if available, using a generic placeholder concept or similar from unsplash
            { id: 7, product_id: 302, image_url: 'https://images.unsplash.com/photo-1603487742131-4160d6e66c6d?auto=format&fit=crop&q=80&w=1000', is_primary: true },
        ],
        variants: [
            { id: 11, product_id: 302, size: '25', color: 'Multi', sku: 'RRS-MU-25', stock_quantity: 50 },
        ],
    },
    // Accessories - Gym Bag
    {
        id: 401,
        category_id: 23, // Accessories > Bags > Gym
        name: 'Pro Active Gym Duffle',
        description: 'Spacious gym bag with separate shoe compartment and water resistant material.',
        base_price: 1599,
        images: [
            { id: 8, product_id: 401, image_url: 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&q=80&w=1000', is_primary: true },
        ],
        variants: [
            { id: 12, product_id: 401, size: 'One Size', color: 'Black', sku: 'PAG-BK-OS', stock_quantity: 100 },
        ],
    },
];
