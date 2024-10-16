// frontend/app/components/NetworkVisualization.tsx

import { FC, useEffect, useRef } from 'react'
import * as d3 from 'd3'
import { StockData } from '../types'

interface NetworkVisualizationProps {
  symbol: string
  data: StockData
}

const NetworkVisualization: FC<NetworkVisualizationProps> = ({ symbol, data }) => {
  const svgRef = useRef<SVGSVGElement | null>(null)

  useEffect(() => {
    if (!data.nodes || !data.links) return

    const svg = d3.select(svgRef.current)
    svg.selectAll('*').remove() // Clear previous content

    const width = parseInt(svg.style('width'))
    const height = parseInt(svg.style('height'))

    const simulation = d3.forceSimulation(data.nodes)
      .force('link', d3.forceLink(data.links).id((d: any) => d.id).distance(50))
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2))

    const link = svg.append('g')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6)
      .selectAll('line')
      .data(data.links)
      .enter().append('line')
      .attr('stroke-width', (d: any) => Math.sqrt(d.value))

    const node = svg.append('g')
      .attr('stroke', '#fff')
      .attr('stroke-width', 1.5)
      .selectAll('circle')
      .data(data.nodes)
      .enter().append('circle')
      .attr('r', 5)
      .attr('fill', (d: any) => d.group === 1 ? 'red' : 'blue')
      .call(drag(simulation))

    node.append('title')
      .text((d: any) => d.id)

    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y)

      node
        .attr('cx', (d: any) => d.x)
        .attr('cy', (d: any) => d.y)
    })

    function drag(simulation: any) {
      function dragstarted(event: any, d: any) {
        if (!event.active) simulation.alphaTarget(0.3).restart()
        d.fx = d.x
        d.fy = d.y
      }

      function dragged(event: any, d: any) {
        d.fx = event.x
        d.fy = event.y
      }

      function dragended(event: any, d: any) {
        if (!event.active) simulation.alphaTarget(0)
        d.fx = null
        d.fy = null
      }

      return d3.drag<SVGCircleElement, any>()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended)
    }

  }, [data])

  return (
    <div className="mb-4">
      <h3 className="text-lg font-semibold mb-2">Network Visualization</h3>
      <svg ref={svgRef} width="100%" height="300"></svg>
    </div>
  )
}

export default NetworkVisualization