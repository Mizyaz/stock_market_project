// frontend/app/components/StockForm.tsx

import { FC } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface StockFormProps {
  symbols: string
  setSymbols: (symbols: string) => void
  stockSet: string | null
  setStockSet: (set: string | null) => void
  freqResolution: number
  setFreqResolution: (val: number) => void
  sectionStart: number
  setSectionStart: (val: number) => void
  sectionEnd: number | null
  setSectionEnd: (val: number | null) => void
  startDate: string
  setStartDate: (val: string) => void
  endDate: string
  setEndDate: (val: string) => void
  interval: string
  setInterval: (val: string) => void
  fetchData: () => void
  loading: boolean
}

const StockForm: FC<StockFormProps> = ({
  symbols,
  setSymbols,
  stockSet,
  setStockSet,
  freqResolution,
  setFreqResolution,
  sectionStart,
  setSectionStart,
  sectionEnd,
  setSectionEnd,
  startDate,
  setStartDate,
  endDate,
  setEndDate,
  interval,
  setInterval,
  fetchData,
  loading
}) => {
  return (
    <div className="flex flex-col space-y-4">
      {/* Stock Set Selection and Custom Symbols */}
      <div className="flex flex-col md:flex-row md:space-x-2 space-y-2 md:space-y-0">
        <Select
          value={stockSet || ''}
          onChange={(value) => {
            setStockSet(value === '' ? null : value)
            if (value !== '') {
              // Optionally, clear custom symbols when a stock set is selected
              setSymbols('')
            }
          }}
        >
          <SelectTrigger className="w-full md:w-[180px]">
            <SelectValue placeholder="Select stock set" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="">Custom</SelectItem>
            <SelectItem value="sp500">S&P 500</SelectItem>
            <SelectItem value="dow">Dow Jones</SelectItem>
            <SelectItem value="nasdaq100">NASDAQ 100</SelectItem>
          </SelectContent>
        </Select>
        <Input
          onChange={(e) => setSymbols(e.target.value)}
          placeholder="Custom symbols (comma-separated)"
          className="w-full md:w-64"
          disabled={!!stockSet}
        />
      </div>

      {/* Frequency Resolution, Section Start, Section End */}
      <div className="flex flex-col md:flex-row md:space-x-2 space-y-2 md:space-y-0">
        <Input
          type="number"
          value={freqResolution}
          onChange={(e) => setFreqResolution(parseFloat(e.target.value))}
          placeholder="Frequency Resolution Multiplier"
          min={1}
          step={0.1}
          className="w-full md:w-64"
        />
        <Input
          type="number"
          value={sectionStart}
          onChange={(e) => setSectionStart(parseInt(e.target.value, 10))}
          placeholder="Section Start"
          min={0}
          className="w-full md:w-32"
        />
        <Input
          type="number"
          value={sectionEnd || ''}
          onChange={(e) => setSectionEnd(e.target.value ? parseInt(e.target.value, 10) : null)}
          placeholder="Section End"
          min={0}
          className="w-full md:w-32"
        />
      </div>

      {/* Date Range Selection */}
      <div className="flex flex-col md:flex-row md:space-x-2 space-y-2 md:space-y-0">
        <Input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          placeholder="Start Date"
          className="w-full md:w-64"
        />
        <Input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          placeholder="End Date"
          className="w-full md:w-64"
        />
      </div>

      {/* Data Interval Selection */}
      <div className="flex flex-col md:flex-row md:space-x-2 space-y-2 md:space-y-0">
        <Select value={interval} onChange={(value) => setInterval(value)}>
          <SelectTrigger className="w-full md:w-[180px]">
            <SelectValue placeholder="Select interval" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="1d">Daily</SelectItem>
            <SelectItem value="1wk">Weekly</SelectItem>
            <SelectItem value="1mo">Monthly</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Analyze Button */}
      <Button onClick={fetchData} disabled={loading} className="w-full">
        {loading ? 'Analyzing...' : 'Analyze'}
      </Button>
    </div>
  )
}

export default StockForm