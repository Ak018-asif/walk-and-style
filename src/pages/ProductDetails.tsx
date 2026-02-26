import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Navbar } from '../components/layout/Navbar';
import { Footer } from '../components/layout/Footer';
import { Button } from '../components/ui/Button';
import { api } from '../api';
import { ProductWithDetails, ProductVariant } from '../types';
import { Check, Heart, Minus, Plus, Share2, ShieldCheck, Truck } from 'lucide-react';

export const ProductDetails: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [product, setProduct] = useState<ProductWithDetails | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [selectedSize, setSelectedSize] = useState<string | null>(null);
    const [selectedColor, setSelectedColor] = useState<string | null>(null);
    const [quantity, setQuantity] = useState(1);
    const [activeImageIndex, setActiveImageIndex] = useState(0);

    useEffect(() => {
        if (id) {
            setIsLoading(true);
            api.getProduct(Number(id)).then(data => {
                setProduct(data);
                // Set default selections if available
                if (data.variants.length > 0) {
                    // Try to pick first size/color
                    // Logic: Get unique sizes and colors
                    const sizes = Array.from(new Set(data.variants.map((v: ProductVariant) => v.size)));
                    if (sizes.length > 0) setSelectedSize(sizes[0]);

                    const colors = Array.from(new Set(data.variants.map((v: ProductVariant) => v.color)));
                    if (colors.length > 0) setSelectedColor(colors[0]);
                }
            }).catch(err => {
                console.error("Failed to load product", err);
            }).finally(() => setIsLoading(false));
        }
    }, [id]);

    if (isLoading) {
        return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
    }

    if (!product) {
        return <div className="min-h-screen flex items-center justify-center">Product not found</div>;
    }

    // Derived state
    const availableSizes = Array.from(new Set(product.variants.map(v => v.size))).sort();
    const availableColors = Array.from(new Set(product.variants.map(v => v.color))).sort();

    // Find currently selected variant to check stock
    const currentVariant = product.variants.find(v => v.size === selectedSize && v.color === selectedColor);
    const isOutOfStock = !currentVariant || currentVariant.stock_quantity === 0;

    // Images
    const images = product.images.length > 0 ? product.images : [{ id: 0, image_url: 'https://via.placeholder.com/800', is_primary: true }];

    return (
        <div className="min-h-screen bg-white">
            <Navbar />

            <main className="pt-24 pb-16 max-w-7xl mx-auto px-4 lg:px-8">
                <div className="flex flex-col lg:flex-row gap-12">
                    {/* Image Gallery */}
                    <div className="lg:w-1/2 space-y-4">
                        <div className="aspect-[4/5] bg-gray-50 rounded-xl overflow-hidden relative">
                            <img
                                src={images[activeImageIndex].image_url}
                                alt={product.name}
                                className="w-full h-full object-cover"
                            />
                            <button className="absolute top-4 right-4 p-2 bg-white rounded-full shadow-md hover:bg-gray-50">
                                <Heart size={20} />
                            </button>
                        </div>
                        <div className="flex gap-4 overflow-x-auto pb-2">
                            {images.map((img, idx) => (
                                <button
                                    key={img.id}
                                    onClick={() => setActiveImageIndex(idx)}
                                    className={`relative w-24 h-24 flex-shrink-0 rounded-lg overflow-hidden border-2 ${activeImageIndex === idx ? 'border-black' : 'border-transparent'}`}
                                >
                                    <img src={img.image_url} alt="" className="w-full h-full object-cover" />
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Product Info */}
                    <div className="lg:w-1/2">
                        <div className="mb-8 border-b border-gray-100 pb-8">
                            <h1 className="text-3xl md:text-4xl font-black italic tracking-tight mb-4">{product.name}</h1>
                            <p className="text-2xl font-bold mb-4">₹{product.base_price.toLocaleString()}</p>
                            <p className="text-gray-600 leading-relaxed">{product.description}</p>
                        </div>

                        {/* Selectors */}
                        <div className="space-y-6 mb-8">
                            {/* Colors */}
                            <div>
                                <h3 className="font-bold text-sm mb-3">Color: <span className="font-normal text-gray-500">{selectedColor}</span></h3>
                                <div className="flex flex-wrap gap-3">
                                    {availableColors.map(color => (
                                        <button
                                            key={color}
                                            onClick={() => setSelectedColor(color)}
                                            className={`px-4 py-2 border rounded-full text-sm font-medium transition-all ${selectedColor === color ? 'border-black bg-black text-white' : 'border-gray-200 hover:border-black'}`}
                                        >
                                            {color}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            {/* Sizes */}
                            <div>
                                <div className="flex justify-between items-center mb-3">
                                    <h3 className="font-bold text-sm">Size: <span className="font-normal text-gray-500">{selectedSize}</span></h3>
                                    <button className="text-xs underline text-gray-500 hover:text-black">Size Guide</button>
                                </div>
                                <div className="flex flex-wrap gap-3">
                                    {availableSizes.map(size => {
                                        // Check if this size is available for the selected color (optional logic for stricter filtering)
                                        // For now just show all sizes present in variants
                                        return (
                                            <button
                                                key={size}
                                                onClick={() => setSelectedSize(size)}
                                                className={`w-12 h-12 flex items-center justify-center border rounded-full text-sm font-medium transition-all ${selectedSize === size ? 'border-black bg-black text-white' : 'border-gray-200 hover:border-black'}`}
                                            >
                                                {size}
                                            </button>
                                        );
                                    })}
                                </div>
                            </div>
                        </div>

                        {/* Actions */}
                        <div className="flex flex-col gap-4 mb-8">
                            <div className="flex items-center gap-4">
                                <div className="flex items-center border border-gray-200 rounded-full">
                                    <button
                                        onClick={() => setQuantity(Math.max(1, quantity - 1))}
                                        className="w-10 h-10 flex items-center justify-center hover:bg-gray-50 rounded-l-full"
                                    >
                                        <Minus size={16} />
                                    </button>
                                    <span className="w-10 text-center font-bold text-sm">{quantity}</span>
                                    <button
                                        onClick={() => setQuantity(quantity + 1)}
                                        className="w-10 h-10 flex items-center justify-center hover:bg-gray-50 rounded-r-full"
                                    >
                                        <Plus size={16} />
                                    </button>
                                </div>
                                <div className="text-sm font-medium text-gray-500">
                                    {isOutOfStock ? 'Out of Stock' : (currentVariant ? `${currentVariant.stock_quantity} in stock` : 'Select options')}
                                </div>
                            </div>

                            <div className="flex gap-4">
                                <Button
                                    size="lg"
                                    className="flex-1"
                                    disabled={isOutOfStock}
                                >
                                    {isOutOfStock ? 'Out of Stock' : 'Add to Cart'}
                                </Button>
                                <Button variant="outline" size="lg" className="w-14 px-0 flex items-center justify-center">
                                    <Share2 size={20} />
                                </Button>
                            </div>
                        </div>

                        {/* Features / Trust */}
                        <div className="grid grid-cols-2 gap-4">
                            <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
                                <Truck size={20} className="text-gray-400" />
                                <span className="text-xs font-bold text-gray-600">Free Shipping</span>
                            </div>
                            <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
                                <ShieldCheck size={20} className="text-gray-400" />
                                <span className="text-xs font-bold text-gray-600">Secure Payment</span>
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
};
