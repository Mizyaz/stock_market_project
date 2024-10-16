// frontend/app/components/StockNetworkVisualization.tsx

"use client"

import { useState, useEffect } from 'react'
import StockForm from './StockForm'
import Guidelines from './Guidelines'
import ErrorMessage from './ErrorMessage'
import StockAnalysisCard from './StockAnalysisCard'
import { GraphData } from '../types'
import { fetchStockAnalysis } from '../lib/api'

const StockNetworkVisualization = () => {
  const [symbols, setSymbols] = useState<string>('AAPL,GOOGL,MSFT')
  const [stockSet, setStockSet] = useState<string | null>(null)
  const [graphData, setGraphData] = useState<GraphData | null>(null)
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)
  const [freqResolution, setFreqResolution] = useState<number>(1.0)
  const [sectionStart, setSectionStart] = useState<number>(0)
  const [sectionEnd, setSectionEnd] = useState<number | null>(null)
  const [startDate, setStartDate] = useState<string>('')
  const [endDate, setEndDate] = useState<string>('')
  const [interval, setInterval] = useState<string>('1d')
  const [guidelines, setGuidelines] = useState<string>('')

  const fetchData = async () => {
    setLoading(true)
    setError(null)
    try {
      const queryParams = new URLSearchParams({
        ...(stockSet ? { stock_set: stockSet } : { symbols }),
        freq_resolution_multiplier: freqResolution.toString(),
        section_start: sectionStart.toString(),
        ...(sectionEnd !== null && { section_end: sectionEnd.toString() }),
        ...(startDate && { start_date: startDate }),
        ...(endDate && { end_date: endDate }),
        interval: interval
      })

      const data: GraphData = await fetchStockAnalysis(queryParams)
      setGraphData(data)

      // Update guidelines based on parameters
      setGuidelines(`Analyzed symbols: ${stockSet || symbols}. Frequency Resolution Multiplier: ${freqResolution}. Date Range: ${startDate || 'N/A'} to ${endDate || 'N/A'}. Data Interval: ${interval}.`)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    // You can trigger fetchData here if needed initially
  }, [])

  return (
    <div className="container mx-auto p-4">
      <StockForm
        symbols={symbols}
        setSymbols={setSymbols}
        stockSet={stockSet}
        setStockSet={setStockSet}
        freqResolution={freqResolution}
        setFreqResolution={setFreqResolution}
        sectionStart={sectionStart}
        setSectionStart={setSectionStart}
        sectionEnd={sectionEnd}
        setSectionEnd={setSectionEnd}
        startDate={startDate}
        setStartDate={setStartDate}
        endDate={endDate}
        setEndDate={setEndDate}
        interval={interval}
        setInterval={setInterval}
        fetchData={fetchData}
        loading={loading}
      />

      {guidelines && <Guidelines content={guidelines} />}

      {error && <ErrorMessage message={error} />}

      {graphData && <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mt-4">
        {Object.entries(graphData).map(([symbol, data]) => (
          <StockAnalysisCard key={symbol} symbol={symbol} data={data} />
        ))}
      </div>}
    </div>
  )
}

export default StockNetworkVisualization
