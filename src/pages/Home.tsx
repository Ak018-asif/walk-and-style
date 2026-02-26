import React, { useEffect, useState } from 'react';
import { Navbar } from '../components/layout/Navbar';
import { Footer } from '../components/layout/Footer';
import { HeroSection } from '../components/features/HeroSection';
import { CategoryGrid } from '../components/features/CategoryGrid';
import { ProductCard } from '../components/ProductCard';
import { api } from '../api';
import { ProductWithDetails } from '../types';
import { Button } from '../components/ui/Button';
import { ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Home: React.FC = () => {
    const [trendingProducts, setTrendingProducts] = useState<ProductWithDetails[]>([]);

    useEffect(() => {
        // Fetch a few products as "trending"
        api.getProducts({ limit: 4 }).then((data) => {
            setTrendingProducts(data);
        }).catch(err => console.error("Failed to fetch trending", err));
    }, []);

    return (
        <div className="min-h-screen bg-white font-sans">
            <Navbar />

            <main className="pt-20">
                <HeroSection />

                <CategoryGrid />

                {/* Trending Section */}
                <section className="py-20 bg-gray-50">
                    <div className="max-w-7xl mx-auto px-4 lg:px-8">
                        <div className="flex justify-between items-end mb-12">
                            <div>
                                <h2 className="text-3xl md:text-4xl font-black italic tracking-tighter mb-4">TRENDING NOW</h2>
                                <p className="text-gray-500">Hot picks from our latest collection</p>
                            </div>
                            <Link to="/products">
                                <Button variant="outline" className="hidden md:flex gap-2">View All <ArrowRight size={18} /></Button>
                            </Link>
                        </div>

                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
                            {trendingProducts.map((product) => (
                                <ProductCard key={product.id} product={product} />
                            ))}
                        </div>

                        <div className="mt-12 text-center md:hidden">
                            <Link to="/products">
                                <Button variant="outline" className="w-full gap-2">View All <ArrowRight size={18} /></Button>
                            </Link>
                        </div>
                    </div>
                </section>

                {/* Newsletter / CTA Section */}
                <section className="py-24 bg-black text-white relative overflow-hidden">
                    <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1556906781-9a412961d28c?auto=format&fit=crop&q=80&w=2000')] bg-cover opacity-20 bg-fixed" />
                    <div className="relative z-10 max-w-4xl mx-auto px-4 text-center">
                        <h2 className="text-4xl md:text-5xl font-black italic tracking-tighter mb-6">JOIN THE MOVEMENT</h2>
                        <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto">
                            Sign up for our newsletter to get exclusive access to drops, events, and special offers.
                        </p>
                        <div className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
                            <input
                                type="email"
                                placeholder="Enter your email"
                                className="flex-1 bg-white/10 backdrop-blur-sm border border-white/20 px-6 py-4 rounded-full text-white placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-white"
                            />
                            <Button size="lg" className="bg-white text-black hover:bg-gray-200">Subscribe</Button>
                        </div>
                    </div>
                </section>
            </main>

            <Footer />
        </div>
    );
};
