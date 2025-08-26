import * as React from 'react'
import { DashboardCard } from '@/components/ui/DashboardCard'

export default function Home() {
  const dashboardItems = [
    {
      title: "Driver Management",
      description: "Track driver profiles, violations, and performance",
      href: "/drivers",
      buttonText: "View Drivers",
      color: "blue" as const
    },
    {
      title: "ETA Prediction", 
      description: "AI-powered delivery time estimation",
      href: "/eta",
      buttonText: "Check ETA",
      color: "green" as const
    },
    {
      title: "Analytics",
      description: "Comprehensive reporting with Metabase", 
      href: "http://localhost:3001",
      buttonText: "Open Metabase",
      color: "purple" as const
    }
  ]

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Logistics Dashboard
        </h2>
        <p className="text-lg text-gray-600">
          AI-Driven Delivery Dashboard with Driver Profiling & Analytics
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
        {dashboardItems.map((item, index) => {
          const { title, description, href, buttonText, color } = item;
          return (
            <DashboardCard 
              key={`dashboard-${index}`}
              {...({ title, description, href, buttonText, color } as any)}
            />
          );
        })}
      </div>
    </div>
  )
}
