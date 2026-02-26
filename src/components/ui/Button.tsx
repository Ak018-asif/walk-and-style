import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
    children,
    className = '',
    variant = 'primary',
    size = 'md',
    isLoading = false,
    disabled,
    ...props
}) => {
    const baseStyles = 'inline-flex items-center justify-center rounded-full font-medium transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed active:scale-95';

    const variants = {
        primary: 'bg-black text-white hover:bg-gray-800 focus:ring-black shadow-lg hover:shadow-xl',
        secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200 focus:ring-gray-500',
        outline: 'border-2 border-gray-200 text-gray-900 hover:border-black focus:ring-black bg-transparent',
        ghost: 'text-gray-600 hover:text-black hover:bg-gray-50 focus:ring-gray-500',
    };

    const sizes = {
        sm: 'px-4 py-1.5 text-sm',
        md: 'px-6 py-2.5 text-base',
        lg: 'px-8 py-3.5 text-lg',
    };

    return (
        <button
            className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
            disabled={disabled || isLoading}
            {...props}
        >
            {isLoading ? (
                <div className="w-5 h-5 border-2 border-current border-t-transparent rounded-full animate-spin mr-2" />
            ) : null}
            {children}
        </button>
    );
};
