import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    icon?: React.ReactNode;
}

export const Input: React.FC<InputProps> = ({
    className = '',
    icon,
    ...props
}) => {
    return (
        <div className="relative">
            {icon && (
                <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none">
                    {icon}
                </div>
            )}
            <input
                className={`w-full rounded-full border border-gray-200 bg-gray-50 px-4 py-2.5 text-sm outline-none transition-all placeholder:text-gray-400 focus:border-black focus:bg-white focus:ring-1 focus:ring-black disabled:cursor-not-allowed disabled:opacity-50 ${icon ? 'pl-10' : ''} ${className}`}
                {...props}
            />
        </div>
    );
};
