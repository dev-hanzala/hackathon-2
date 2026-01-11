import type { Metadata } from 'next';
import { Providers } from './providers';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import '@/styles/globals.css';

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A simple and elegant todo application',
  viewport: 'width=device-width, initial-scale=1',
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head />
      <body>
        <ErrorBoundary>
          <Providers>{children}</Providers>
        </ErrorBoundary>
      </body>
    </html>
  );
}
