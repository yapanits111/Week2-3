import React from 'react'

interface PageProps {
  params: {
    id: string
  }
}

export default function DriverProfilePage({ params }: PageProps) {
  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Driver Profile</h1>
        <p className="text-gray-600 mt-2">Driver ID: {params.id}</p>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Profile Details</h2>
        <p className="text-gray-600">Driver profile for ID: {params.id}</p>
        <p className="text-gray-500 mt-2">This page will show detailed driver information, drug tests, violations, and performance metrics.</p>
      </div>
    </div>
  )
}