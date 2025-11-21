import React from 'react';

export const ScrollArea = ({ children, className = '' }) => {
  return (
    <div className={`overflow-y-auto ${className}`} style={{ height: '100%' }}>
      {children}
    </div>
  );
};
