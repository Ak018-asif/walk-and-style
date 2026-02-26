import React from 'react';
import { ArrowRight } from 'lucide-react';
import { Button } from '../ui/Button';
import { Link } from 'react-router-dom';

export const HeroSection: React.FC = () => {
    return (
        <div className="relative h-[80vh] w-full bg-gray-900 overflow-hidden flex items-center">
            {/* Background Image */}
            <div className="absolute inset-0 z-0">
                <img
                    src="https://images.unsplash.com/photo-1549298916-b41d501d3772?auto=format&fit=crop&q=80&w=2000"
                    alt="Hero Background"
                    className="w-full h-full object-cover opacity-60"
                />
                <div className="absolute inset-0 bg-gradient-to-r from-black/80 to-transparent" />
            </div>

            {/* Content */}
            <div className="relative z-10 max-w-7xl mx-auto px-4 lg:px-8 text-white">
                <div className="max-w-2xl animate-in slide-in-from-bottom-10 duration-700">
                    <span className="inline-block py-1 px-3 rounded-full bg-white/20 backdrop-blur-sm text-sm font-bold tracking-wider mb-6 border border-white/30">
                        NEW COLLECTION 2024
                    </span>
                    <h1 className="text-5xl md:text-7xl font-black tracking-tight mb-6 leading-tight">
                        STEP INTO <br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400">THE FUTURE.</span>
                    </h1>
                    <p className="text-lg md:text-xl text-gray-300 mb-8 leading-relaxed max-w-lg">
                        Experience the perfect blend of comfort and style with our premium footwear collection for the whole family.
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4">
                        <Link to="/products">
                            <Button size="lg" className="w-full sm:w-auto gap-2">
                                Shop Now <ArrowRight size={20} />
                            </Button>
                        </Link>
                        <Link to="/products?category=1">
                            <Button variant="outline" size="lg" className="w-full sm:w-auto border-white text-white hover:bg-white hover:text-black hover:border-white">
                                View Men's
                            </Button>
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
};
