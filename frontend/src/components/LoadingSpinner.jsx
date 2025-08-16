import React from 'react';
import { Loader2 } from 'lucide-react';

const LoadingSpinner = ({ size = "default", text = "Loading..." }) => {
  const sizeClasses = {
    small: "h-4 w-4",
    default: "h-6 w-6", 
    large: "h-8 w-8"
  };

  return (
    <div className="flex items-center justify-center gap-2 text-white/70">
      <Loader2 className={`${sizeClasses[size]} animate-spin`} />
      <span className="text-sm">{text}</span>
    </div>
  );
};

export default LoadingSpinner;