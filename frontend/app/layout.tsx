import React from 'react'
import './globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Logistics Dashboard',
  description: 'AI-Driven Delivery Dashboard with Driver Profiling',
}

export default function RootLayout({
  children,
}: {
  children: any
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gray-50">
          <nav className="bg-white shadow-sm border-b">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16">
                <div className="flex items-center">
                  <h1 className="text-xl font-semibold text-gray-900">
                    Logistics Dashboard
                  </h1>
                </div>
                <div className="flex items-center space-x-4">
                  <a href="/" className="text-gray-700 hover:text-gray-900">Dashboard</a>
                  <a href="/drivers" className="text-gray-700 hover:text-gray-900">Drivers</a>
                  <a href="/analytics" className="text-gray-700 hover:text-gray-900">Analytics</a>
                </div>
              </div>
            </div>
          </nav>
          <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            {children}
          </main>
        </div>
      </body>
    </html>
  )
}
