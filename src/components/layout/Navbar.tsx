import React, { useState, useEffect } from 'react';
import { Search, ShoppingBag, Menu, X, User, Heart } from 'lucide-react';
import { api } from '../../api';
import { Category } from '../../types';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Badge } from '../ui/Badge';
import { Link } from 'react-router-dom';

interface NavbarProps {
    cartCount?: number;
}

export const Navbar: React.FC<NavbarProps> = ({ cartCount = 0 }) => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [isSearchOpen, setIsSearchOpen] = useState(false);
    const [categories, setCategories] = useState<Category[]>([]);

    useEffect(() => {
        // Fetch top-level categories (or tree if endpoint available, but we implemented /tree)
        // The previous mocked CATEGORIES was flat list. The new API /categories/ returns flat list.
        // We want top level ones.
        api.getCategories().then((data: Category[]) => {
            setCategories(data);
        }).catch(err => console.error("Failed to fetch categories", err));
    }, []);

    // Filter top-level categories
    const topCategories = categories.filter(c => c.parent_id === null);

    return (
        <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100 transition-all duration-300">
            <div className="max-w-7xl mx-auto px-4 lg:px-8">
                <div className="flex items-center justify-between h-20">

                    {/* Mobile Menu Button */}
                    <button
                        className="lg:hidden p-2 -ml-2 text-gray-600 hover:text-black"
                        onClick={() => setIsMenuOpen(!isMenuOpen)}
                    >
                        {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
                    </button>

                    {/* Logo */}
                    <Link to="/" className="text-2xl font-black tracking-tighter italic mr-8">
                        WALK <span className="text-gray-400">n</span> STYLE
                    </Link>

                    {/* Desktop Navigation */}
                    <nav className="hidden lg:flex items-center gap-8">
                        {topCategories.map((category) => (
                            <div key={category.id} className="group relative">
                                <Link
                                    to={`/products?category=${category.id}`}
                                    className="text-sm font-bold uppercase tracking-wide hover:text-gray-600 py-8 inline-block"
                                >
                                    {category.name}
                                </Link>
                                {/* Mega Menu Dropdown (Simplified for now, can be expanded) */}
                                <div className="absolute top-full left-0 w-64 bg-white shadow-xl rounded-b-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 transform origin-top translate-y-2 group-hover:translate-y-0 border border-gray-100 p-4 z-50">
                                    <div className="flex flex-col gap-2">
                                        {categories.filter(c => c.parent_id === category.id).map(sub => (
                                            <Link
                                                key={sub.id}
                                                to={`/products?category=${sub.id}`}
                                                className="text-sm text-gray-600 hover:text-black py-1 block hover:pl-2 transition-all"
                                            >
                                                {sub.name}
                                            </Link>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </nav>

                    {/* Right Layout */}
                    <div className="flex items-center gap-2 lg:gap-4 ml-auto">
                        {/* Search Bar (Desktop) */}
                        <div className="hidden lg:block w-64">
                            <Input
                                placeholder="Search products..."
                                icon={<Search size={18} />}
                            />
                        </div>

                        {/* Mobile Search Toggle */}
                        <button
                            className="lg:hidden p-2 text-gray-600 hover:text-black"
                            onClick={() => setIsSearchOpen(!isSearchOpen)}
                        >
                            <Search size={22} />
                        </button>

                        <button className="p-2 text-gray-600 hover:text-black hidden sm:block">
                            <User size={22} />
                        </button>

                        <button className="p-2 text-gray-600 hover:text-black hidden sm:block">
                            <Heart size={22} />
                        </button>

                        <button className="p-2 text-black hover:opacity-70 relative">
                            <ShoppingBag size={22} />
                            {cartCount > 0 && (
                                <span className="absolute top-0 right-0 bg-black text-white text-[10px] w-4 h-4 flex items-center justify-center rounded-full font-bold">
                                    {cartCount}
                                </span>
                            )}
                        </button>
                    </div>
                </div>

                {/* Mobile Search Bar */}
                {isSearchOpen && (
                    <div className="lg:hidden py-4 px-2 border-t border-gray-100 animate-in slide-in-from-top-2">
                        <Input
                            autoFocus
                            placeholder="Search products..."
                            icon={<Search size={18} />}
                        />
                    </div>
                )}
            </div>

            {/* Mobile Menu Overlay */}
            {isMenuOpen && (
                <div className="fixed inset-0 top-20 z-40 bg-white lg:hidden overflow-y-auto w-full animate-in slide-in-from-left-5">
                    <div className="p-4 space-y-4">
                        {topCategories.map((category) => (
                            <div key={category.id} className="border-b border-gray-100 pb-4">
                                <Link
                                    to={`/products?category=${category.id}`}
                                    className="block text-lg font-bold mb-2"
                                    onClick={() => setIsMenuOpen(false)}
                                >
                                    {category.name}
                                </Link>
                                <div className="pl-4 flex flex-col gap-2">
                                    {categories.filter(c => c.parent_id === category.id).map(sub => (
                                        <Link
                                            key={sub.id}
                                            to={`/products?category=${sub.id}`}
                                            className="text-gray-600 text-sm"
                                            onClick={() => setIsMenuOpen(false)}
                                        >
                                            {sub.name}
                                        </Link>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </header>
    );
};
