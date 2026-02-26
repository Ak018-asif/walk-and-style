import React from 'react';

interface BadgeProps {
    children: React.ReactNode;
    variant?: 'default' | 'outline' | 'destructive' | 'secondary';
    className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
    children,
    variant = 'default',
    className = '',
}) => {
    const baseStyles = 'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2';

    const variants = {
        default: 'bg-black text-white hover:bg-gray-800',
        secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200',
        destructive: 'bg-red-500 text-white hover:bg-red-600',
        outline: 'text-gray-900 border border-gray-200',
    };

    return (
        <span className={`${baseStyles} ${variants[variant]} ${className}`}>
            {children}
        </span>
    );
};
