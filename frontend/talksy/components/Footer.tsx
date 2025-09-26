'use client';

export default function Footer() {
  return (
    <footer className="fixed bottom-0 w-full bg-[var(--color-background)] border-t border-[var(--color-foreground-muted)] py-2 text-center text-sm text-[var(--color-foreground-muted)]">
      <div className="container mx-auto px-4">
        <p>
          Talksy - Your Private Voice Assistant &copy; {new Date().getFullYear()}
        </p>
        <p className="text-xs mt-1">
          All processing happens locally. Your privacy is guaranteed.
        </p>
      </div>
    </footer>
  );
} 