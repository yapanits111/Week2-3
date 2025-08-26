'use client'

import React, { useState } from 'react'

interface ETAResult {
  eta_minutes: number
  message: string
  distance_km: number
}

interface ModelStatus {
  status: string
  model_trained: boolean
}

export default function ETAPage() {
  const [coordinates, setCoordinates] = useState({
    currentLat: '14.5995',
    currentLng: '120.9842', 
    dropoffLat: '14.6091',
    dropoffLng: '121.0223'
  })
  const [result, setResult] = useState<ETAResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [training, setTraining] = useState(false)
  const [modelStatus, setModelStatus] = useState<ModelStatus | null>(null)

  const predictETA = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:5000/predict_eta', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          current_lat: parseFloat(coordinates.currentLat),
          current_lng: parseFloat(coordinates.currentLng),
          dropoff_lat: parseFloat(coordinates.dropoffLat),
          dropoff_lng: parseFloat(coordinates.dropoffLng)
        })
      })

      if (!response.ok) {
        throw new Error('Failed to predict ETA')
      }

      const data = await response.json()
      setResult({
        eta_minutes: data.eta_minutes,
        distance_km: data.distance_km,
        message: data.message
      })
    } catch (error) {
      console.error('Error predicting ETA:', error)
      alert('Error predicting ETA. Make sure the AI service is running.')
    } finally {
      setLoading(false)
    }
  }

  const trainModel = async () => {
    setTraining(true)
    try {
      const response = await fetch('http://localhost:5000/train_model', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      })

      if (!response.ok) {
        throw new Error('Failed to train model')
      }

      const data = await response.json()
      alert(`Model trained successfully! MAE: ${data.results.mae.toFixed(2)} minutes`)
      checkModelStatus()
    } catch (error) {
      console.error('Error training model:', error)
      alert('Error training model. Make sure the AI service is running.')
    } finally {
      setTraining(false)
    }
  }

  const checkModelStatus = async () => {
    try {
      const response = await fetch('http://localhost:5000/health')
      if (response.ok) {
        const data = await response.json()
        setModelStatus(data)
      }
    } catch (error) {
      console.error('Error checking model status:', error)
    }
  }

  React.useEffect(() => {
    checkModelStatus()
  }, [])

  const handleInputChange = (field: string, value: string) => {
    setCoordinates(prev => ({ ...prev, [field]: value }))
  }

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="max-w-2xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">ETA Prediction</h1>
          <p className="text-gray-600 mt-2">AI-powered delivery time estimation</p>
        </div>

        <div className="bg-white shadow rounded-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Calculate Delivery ETA</h2>
            <div className="flex items-center space-x-2">
              {modelStatus && (
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  modelStatus.model_trained 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {modelStatus.model_trained ? 'Model Ready' : 'Model Not Trained'}
                </span>
              )}
              <button
                onClick={trainModel}
                disabled={training}
                className="bg-green-500 text-white px-3 py-1 rounded text-sm hover:bg-green-600 disabled:opacity-50"
              >
                {training ? 'Training...' : 'Train Model'}
              </button>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div>
              <h3 className="font-medium text-gray-900 mb-3">Current Location</h3>
              <div className="space-y-2">
                <input
                  type="text"
                  placeholder="Latitude"
                  value={coordinates.currentLat}
                  onChange={(e: any) => handleInputChange('currentLat', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <input
                  type="text"
                  placeholder="Longitude"
                  value={coordinates.currentLng}
                  onChange={(e: any) => handleInputChange('currentLng', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <div>
              <h3 className="font-medium text-gray-900 mb-3">Destination</h3>
              <div className="space-y-2">
                <input
                  type="text"
                  placeholder="Latitude"
                  value={coordinates.dropoffLat}
                  onChange={(e: any) => handleInputChange('dropoffLat', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <input
                  type="text"
                  placeholder="Longitude"
                  value={coordinates.dropoffLng}
                  onChange={(e: any) => handleInputChange('dropoffLng', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
          </div>

          <button
            onClick={predictETA}
            disabled={loading || !modelStatus?.model_trained}
            className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Calculating...' : !modelStatus?.model_trained ? 'Train Model First' : 'Predict ETA'}
          </button>

          {result && (
            <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <h3 className="font-medium text-green-900 mb-2">Prediction Result</h3>
              <div className="space-y-2 text-green-800">
                <p><strong>ETA:</strong> {result.eta_minutes.toFixed(1)} minutes</p>
                <p><strong>Distance:</strong> {result.distance_km.toFixed(1)} km</p>
                <p><strong>Status:</strong> {result.message}</p>
              </div>
            </div>
          )}

          <div className="mt-6 p-4 bg-gray-50 rounded-lg">
            <h3 className="font-medium text-gray-900 mb-2">Sample Coordinates (Manila Area)</h3>
            <div className="text-sm text-gray-600 space-y-1">
              <p><strong>Makati CBD:</strong> 14.5547, 121.0244</p>
              <p><strong>BGC:</strong> 14.5176, 121.0509</p>
              <p><strong>Ortigas:</strong> 14.5866, 121.0611</p>
              <p><strong>Quezon City:</strong> 14.6760, 121.0437</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
