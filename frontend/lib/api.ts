// frontend/app/lib/api.ts

import { GraphData } from '../types'

export const fetchStockAnalysis = async (params: URLSearchParams): Promise<GraphData> => {
  const response = await fetch(`http://localhost:8000/analyze?${params.toString()}`)
  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || 'Failed to fetch data')
  }

  const data: GraphData = await response.json()
  return data
}