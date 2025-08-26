'use client'

import React, { useState, useEffect } from 'react'

interface Driver {
  id: number
  name: string
  license_number: string
  contact: string
  status: string
  violations_count?: number
  average_rating?: number
}

export default function DriversPage() {
  const [drivers, setDrivers] = useState<Driver[]>([])
  const [selectedDriver, setSelectedDriver] = useState<Driver | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Mock data for now - replace with actual API call
    setTimeout(() => {
      setDrivers([
        {
          id: 1,
          name: "Juan Dela Cruz",
          license_number: "LIC123456789",
          contact: "+639123456781",
          status: "active",
          violations_count: 2,
          average_rating: 4.5
        },
        {
          id: 2,
          name: "Maria Santos",
          license_number: "LIC987654321", 
          contact: "+639123456782",
          status: "active",
          violations_count: 0,
          average_rating: 4.8
        },
        {
          id: 3,
          name: "Pedro Rodriguez",
          license_number: "LIC555666777",
          contact: "+639123456783", 
          status: "suspended",
          violations_count: 5,
          average_rating: 3.2
        }
      ])
      setLoading(false)
    }, 1000)
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800'
      case 'suspended': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-96">
        <div className="text-xl text-gray-600">Loading drivers...</div>
      </div>
    )
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Driver Management</h1>
        <p className="text-gray-600 mt-2">Manage driver profiles and performance</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Driver List */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">All Drivers</h2>
          <div className="space-y-4">
            {drivers.map((driver) => (
              <div 
                key={driver.id}
                className={`p-4 border rounded-lg cursor-pointer transition-colors hover:bg-gray-50 ${
                  selectedDriver?.id === driver.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
                }`}
                onClick={() => setSelectedDriver(driver)}
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium text-gray-900">{driver.name}</h3>
                    <p className="text-sm text-gray-500">{driver.license_number}</p>
                    <p className="text-sm text-gray-500">{driver.contact}</p>
                  </div>
                  <div className="text-right">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(driver.status)}`}>
                      {driver.status}
                    </span>
                    <div className="mt-2 text-sm text-gray-600">
                      Rating: {driver.average_rating?.toFixed(1) || 'N/A'}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Driver Details */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Driver Details</h2>
          {selectedDriver ? (
            <div>
              <div className="mb-6">
                <h3 className="text-lg font-medium text-gray-900">{selectedDriver.name}</h3>
                <p className="text-gray-600">{selectedDriver.license_number}</p>
                <span className={`inline-block mt-2 px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(selectedDriver.status)}`}>
                  {selectedDriver.status}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">
                    {selectedDriver.average_rating?.toFixed(1) || 'N/A'}
                  </div>
                  <div className="text-sm text-gray-600">Average Rating</div>
                </div>
                <div className="bg-orange-50 p-4 rounded-lg">
                  <div className="text-2xl font-bold text-orange-600">
                    {selectedDriver.violations_count || 0}
                  </div>
                  <div className="text-sm text-gray-600">Violations</div>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Contact Information</h4>
                  <p className="text-gray-600">{selectedDriver.contact}</p>
                </div>
                
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Recent Activity</h4>
                  <div className="text-sm text-gray-500 space-y-1">
                    <p>• Last delivery completed: 2 hours ago</p>
                    <p>• Current status: Available</p>
                    <p>• Next scheduled delivery: Tomorrow 9:00 AM</p>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center text-gray-500 py-8">
              Select a driver to view details
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
