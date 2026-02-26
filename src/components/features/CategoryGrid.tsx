import React from 'react';
import { ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import { CATEGORIES } from '../../data/mockData';

export const CategoryGrid: React.FC = () => {
    // Select specific categories to feature: Men(1), Women(11), Kids(16), Accessories(21)
    const featuredIds = [1, 11, 16, 21];
    const featuredCategories = CATEGORIES.filter(c => featuredIds.includes(c.id));

    const getCategoryImage = (id: number) => {
        switch (id) {
            case 1: return 'https://images.unsplash.com/photo-1488161628813-99c974c76949?auto=format&fit=crop&q=80&w=800'; // Men
            case 11: return 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&q=80&w=800'; // Women
            case 16: return 'https://images.unsplash.com/photo-1514989940723-e887532d5588?auto=format&fit=crop&q=80&w=800'; // Kids
            case 21: return 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&q=80&w=800'; // Accessories
            default: return '';
        }
    };

    return (
        <section className="py-20 bg-white">
            <div className="max-w-7xl mx-auto px-4 lg:px-8">
                <div className="flex justify-between items-end mb-12">
                    <div>
                        <h2 className="text-3xl md:text-4xl font-black italic tracking-tighter mb-4">SHOP BY CATEGORY</h2>
                        <p className="text-gray-500">Explore our wide range of collections</p>
                    </div>
                    <Link to="/products" className="group flex items-center gap-2 font-bold text-sm hidden md:flex">
                        VIEW ALL <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
                    </Link>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {featuredCategories.map((category) => (
                        <Link
                            key={category.id}
                            to={`/products?category=${category.id}`}
                            className="group relative h-96 overflow-hidden rounded-xl cursor-pointer"
                        >
                            <img
                                src={getCategoryImage(category.id)}
                                alt={category.name}
                                className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                            />
                            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-80 group-hover:opacity-90 transition-opacity" />
                            <div className="absolute bottom-0 left-0 p-6 w-full transform translate-y-2 group-hover:translate-y-0 transition-transform">
                                <h3 className="text-2xl font-bold text-white mb-2">{category.name}</h3>
                                <span className="inline-flex items-center gap-2 text-white text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity delay-100">
                                    Shop Now <ArrowRight size={16} />
                                </span>
                            </div>
                        </Link>
                    ))}
                </div>
            </div>
        </section>
    );
};
