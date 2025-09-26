'use client';

export default function Header() {
  return (
    <header className="fixed w-full top-0 border-b border-[var(--color-foreground-muted)] bg-[var(--color-background)] z-10">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-violet-500">
            Talksy
          </span>
          <span className="text-xs bg-blue-500 text-white px-2 py-1 rounded-full">
            Beta
          </span>
        </div>
        
        <div className="flex items-center space-x-4">
          <span className="text-sm text-[var(--color-foreground-muted)]">
            Your Private Voice Assistant
          </span>
        </div>
      </div>
    </header>
  );
} 