import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Home } from './pages/Home';
import { ProductListing } from './pages/ProductListing';
import { ProductDetails } from './pages/ProductDetails';

// Placeholders for other pages
const Cart = () => <div className="pt-32 text-center text-2xl font-bold">Cart Page (Coming Soon)</div>;

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/products" element={<ProductListing />} />
      <Route path="/product/:id" element={<ProductDetails />} />
      <Route path="/cart" element={<Cart />} />
    </Routes>
  );
};

export default App;
