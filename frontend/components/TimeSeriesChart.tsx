// frontend/app/components/TimeSeriesChart.tsx

import { FC } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { StockData } from '../types'

interface TimeSeriesChartProps {
  symbol: string
  data: StockData
}

const TimeSeriesChart: FC<TimeSeriesChartProps> = ({ symbol, data }) => {
  const prices = data.prices
  const sma = data.indicators.sma
  const bollingerBands = data.indicators.bollinger_bands

  // Prepare data for Recharts
  const chartData = prices.map((price, index) => ({
    name: index,
    price: price,
    sma: sma ? sma[index] : null,
    upperband: bollingerBands?.upperband[index] || null,
    middleband: bollingerBands?.middleband[index] || null,
    lowerband: bollingerBands?.lowerband[index] || null,
  }))

  return (
    <div className="mb-4">
      <h3 className="text-lg font-semibold mb-2">Time Series with Indicators</h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={chartData}>
          <XAxis dataKey="name" hide />
          <YAxis domain={['auto', 'auto']} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="price" stroke="#8884d8" dot={false} name="Price" />
          {sma && <Line type="monotone" dataKey="sma" stroke="#82ca9d" dot={false} name="SMA" />}
          {bollingerBands && <Line type="monotone" dataKey="upperband" stroke="#ff7300" dot={false} name="Upper Bollinger Band" />}
          {bollingerBands && <Line type="monotone" dataKey="middleband" stroke="#387908" dot={false} name="Middle Bollinger Band" />}
          {bollingerBands && <Line type="monotone" dataKey="lowerband" stroke="#ff7300" dot={false} name="Lower Bollinger Band" />}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default TimeSeriesChart