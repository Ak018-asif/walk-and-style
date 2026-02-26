import React from 'react';
import { Facebook, Instagram, Twitter, MapPin, Mail, Phone } from 'lucide-react';

export const Footer: React.FC = () => {
    return (
        <footer className="bg-gray-50 pt-16 pb-8 border-t border-gray-200">
            <div className="max-w-7xl mx-auto px-4 lg:px-8">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-12">

                    {/* Brand Info */}
                    <div className="space-y-6">
                        <h3 className="text-2xl font-black italic tracking-tighter">WALK n STYLE</h3>
                        <p className="text-gray-500 text-sm leading-relaxed">
                            Step into comfort and style. We bring you the finest collection of footwear for men, women, and kids. Experiences that last.
                        </p>
                        <div className="flex items-center gap-4">
                            <a href="#" className="w-10 h-10 rounded-full bg-white border border-gray-200 flex items-center justify-center text-gray-600 hover:bg-black hover:text-white hover:border-black transition-all">
                                <Facebook size={18} />
                            </a>
                            <a href="#" className="w-10 h-10 rounded-full bg-white border border-gray-200 flex items-center justify-center text-gray-600 hover:bg-black hover:text-white hover:border-black transition-all">
                                <Instagram size={18} />
                            </a>
                            <a href="#" className="w-10 h-10 rounded-full bg-white border border-gray-200 flex items-center justify-center text-gray-600 hover:bg-black hover:text-white hover:border-black transition-all">
                                <Twitter size={18} />
                            </a>
                        </div>
                    </div>

                    {/* Quick Links */}
                    <div>
                        <h4 className="font-bold text-gray-900 mb-6 uppercase text-sm tracking-wider">Shop</h4>
                        <ul className="space-y-3 text-sm text-gray-600">
                            <li><a href="#" className="hover:text-black transition-colors">New Arrivals</a></li>
                            <li><a href="#" className="hover:text-black transition-colors">Men's Collection</a></li>
                            <li><a href="#" className="hover:text-black transition-colors">Women's Collection</a></li>
                            <li><a href="#" className="hover:text-black transition-colors">Kids' World</a></li>
                            <li><a href="#" className="hover:text-black transition-colors">Accessories</a></li>
                        </ul>
                    </div>

                    {/* Support */}
                    <div>
                        <h4 className="font-bold text-gray-900 mb-6 uppercase text-sm tracking-wider">Support</h4>
                        <ul className="space-y-3 text-sm text-gray-600">
                            <li><a href="#" className="hover:text-black transition-colors">Order Status</a></li>
                            <li><a href="#" className="hover:text-black transition-colors">Shipping & Delivery</a></li>
                            <li><a href="#" className="hover:text-black transition-colors">Returns & Exchanges</a></li>
                            <li><a href="#" className="hover:text-black transition-colors">Size Guide</a></li>
                            <li><a href="#" className="hover:text-black transition-colors">FAQ</a></li>
                        </ul>
                    </div>

                    {/* Contact */}
                    <div>
                        <h4 className="font-bold text-gray-900 mb-6 uppercase text-sm tracking-wider">Contact</h4>
                        <ul className="space-y-4 text-sm text-gray-600">
                            <li className="flex items-start gap-3">
                                <MapPin size={18} className="shrink-0 mt-0.5" />
                                <span>123 Fashion Street, Style District, NY 10001</span>
                            </li>
                            <li className="flex items-center gap-3">
                                <Phone size={18} className="shrink-0" />
                                <span>+1 (800) 123-4567</span>
                            </li>
                            <li className="flex items-center gap-3">
                                <Mail size={18} className="shrink-0" />
                                <span>support@walknstyle.com</span>
                            </li>
                        </ul>
                    </div>
                </div>

                <div className="border-t border-gray-200 pt-8 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-gray-500 font-medium">
                    <p>&copy; {new Date().getFullYear()} Walk n Style. All rights reserved.</p>
                    <div className="flex gap-6">
                        <a href="#" className="hover:text-black">Privacy Policy</a>
                        <a href="#" className="hover:text-black">Terms of Service</a>
                    </div>
                </div>
            </div>
        </footer>
    );
};
