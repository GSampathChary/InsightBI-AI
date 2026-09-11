import './globals.css';
import React from 'react';

export const metadata = {
  title: 'InsightBI AI — Enterprise AI Business Intelligence',
  description: 'Transform business raw data into analytics, forecasting, Power BI insights, and natural language AI Copilot decisions.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-gray-100 antialiased selection:bg-blue-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
