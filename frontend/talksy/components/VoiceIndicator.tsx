'use client';

import { useRef, useEffect } from 'react';

interface VoiceIndicatorProps {
  isActive: boolean;
}

export default function VoiceIndicator({ isActive }: VoiceIndicatorProps) {
  return (
    <div className="flex justify-center items-center">
      {isActive ? (
        <AudioVisualizer />
      ) : (
        <div className="flex items-center space-x-1">
          {[...Array(5)].map((_, i) => (
            <div
              key={i}
              className="w-1 h-3 bg-[#999] opacity-50 rounded-full"
            />
          ))}
        </div>
      )}
    </div>
  );
}

function AudioVisualizer() {
  const MAX_BARS = 5;
  const barRefs = useRef<(HTMLDivElement | null)[]>([]);
  
  useEffect(() => {
    // Initialize bar heights
    barRefs.current.forEach((bar) => {
      if (!bar) return;
      animateBar(bar);
    });
    
    const intervals: number[] = [];
    
    // Animate each bar with a slightly different interval
    barRefs.current.forEach((bar, i) => {
      if (!bar) return;
      const interval = window.setInterval(() => {
        animateBar(bar);
      }, 500 + i * 100);
      intervals.push(interval);
    });
    
    return () => {
      intervals.forEach(clearInterval);
    };
  }, []);
  
  function animateBar(bar: HTMLDivElement) {
    const height = Math.floor(Math.random() * 25) + 5; // Random height between 5-30px
    bar.style.height = `${height}px`;
  }
  
  return (
    <div className="flex items-end space-x-1 h-8">
      {[...Array(MAX_BARS)].map((_, i) => (
        <div
          key={i}
          ref={(el) => (barRefs.current[i] = el)}
          className="w-1 bg-blue-500 rounded-full transition-all duration-300"
          style={{ height: '3px' }}
        />
      ))}
    </div>
  );
} 