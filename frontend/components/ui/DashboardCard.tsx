import * as React from 'react'

interface DashboardCardProps {
  title: string
  description: string
  href: string
  buttonText: string
  color: 'blue' | 'green' | 'purple'
}

const colorClasses = {
  blue: 'bg-blue-500 hover:bg-blue-600',
  green: 'bg-green-500 hover:bg-green-600', 
  purple: 'bg-purple-500 hover:bg-purple-600'
}

export function DashboardCard({ title, description, href, buttonText, color }: DashboardCardProps) {
  const isExternal = href.startsWith('http')
  
  return (
    <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
      <h3 className="text-xl font-semibold mb-2 text-gray-900">{title}</h3>
      <p className="text-gray-600 mb-4">{description}</p>
      <a 
        href={href} 
        className={`inline-block text-white px-4 py-2 rounded transition-colors ${colorClasses[color]}`}
        {...(isExternal && { target: '_blank', rel: 'noopener noreferrer' })}
      >
        {buttonText}
      </a>
    </div>
  )
}
