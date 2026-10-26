import { useState } from 'react';

export function ThemeToggle() {
  const [theme, setTheme] = useState(() => document.documentElement.dataset.theme || 'light');

  function toggleTheme() {
    const nextTheme = theme === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = nextTheme;
    setTheme(nextTheme);
    try { localStorage.setItem('theme', nextTheme); } catch { /* Theme still works without storage. */ }
  }

  return (
    <button className="theme-toggle" onClick={toggleTheme} aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}>
      <span aria-hidden="true">{theme === 'light' ? '◐' : '◑'}</span>
      <span>{theme === 'light' ? 'Light' : 'Dark'}</span>
    </button>
  );
}
