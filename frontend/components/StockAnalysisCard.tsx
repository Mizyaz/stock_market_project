// frontend/app/components/StockAnalysisCard.tsx

import { FC, useEffect, useRef } from 'react'
import { StockData } from '../types'
import NetworkVisualization from './NetworkVisualization'
import TimeSeriesChart from './TimeSeriesChart'
import ImageDisplay from './ImageDisplay'
import { Button } from "@/components/ui/button"

interface StockAnalysisCardProps {
  symbol: string
  data: StockData
}

const StockAnalysisCard: FC<StockAnalysisCardProps> = ({ symbol, data }) => {
  const timestamp = useRef<number>(Date.now())

  const handleRefresh = () => {
    // Force refresh by updating the timestamp
    timestamp.current = Date.now()
    // Note: The parent component should handle state update to trigger re-fetch
    // Here, assuming that adding a query param with timestamp suffices
  }

  return (
    <div className="p-4 border rounded shadow">
      <h2 className="text-xl font-bold mb-2">{symbol} Analysis</h2>
      
      {/* Network Visualization */}
      <NetworkVisualization symbol={symbol} data={data} />

      {/* Time Series with Indicators */}
      <TimeSeriesChart symbol={symbol} data={data} />

      {/* Mel Spectrogram */}
      <ImageDisplay
        src={`http://localhost:8000${data.spectrogram_image}`}
        alt={`${symbol} Mel Spectrogram`}
        width={400}
        height={160}
        title="Mel Spectrogram"
      />

      {/* MFCCs */}
      <ImageDisplay
        src={`http://localhost:8000${data.mfccs_image}`}
        alt={`${symbol} MFCCs`}
        width={400}
        height={240}
        title="MFCCs"
      />

      {/* Time-Frequency Representation */}
      <ImageDisplay
        src={`http://localhost:8000${data.time_frequency_image}`}
        alt={`${symbol} Time-Frequency`}
        width={400}
        height={160}
        title="Time-Frequency Representation"
      />

      {/* Refresh Graphs Button */}
      <Button
        onClick={handleRefresh}
        className="mt-4"
        onClickCapture={() => {
          // Implement refresh logic by updating the image URLs with timestamp
        }}
      >
        Refresh Graphs
      </Button>
    </div>
  )
}

export default StockAnalysisCard