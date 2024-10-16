// frontend/app/types/index.ts

export interface Node extends d3.SimulationNodeDatum {
    id: string
    group: number
  }
  
  export interface Link extends d3.SimulationLinkDatum<Node> {
    value: number
  }
  
  export interface StockData {
    nodes: Node[]
    links: Link[]
    time_series_image: string
    spectrogram_image: string
    mfccs_image: string
    time_frequency_image: string
    prices: number[]
    mfccs: number[][]
    section_start: number
    section_end: number | null
    indicators: {
      sma: number[] | null
      rsi: number[] | null
      macd: {
        macd: number[] | null
        macdsignal: number[] | null
        macdhist: number[] | null
      }
      bollinger_bands: {
        upperband: number[] | null
        middleband: number[] | null
        lowerband: number[] | null
      }
    }
  }
  
  export interface GraphData {
    [symbol: string]: StockData
  }