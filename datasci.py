import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "/components/ui/card"
import { Button } from "/components/ui/button"
import { Input } from "/components/ui/input"
import { Label } from "/components/ui/label"

type DataPoint = {
  label: string
  value: number
}

export default function BarChart() {
  const [inputData, setInputData] = useState('')
  const [chartData, setChartData] = useState<DataPoint[]>([])
  const [error, setError] = useState('')

  const parseInputData = () => {
    try {
      setError('')
      
      // Parse CSV input (label,value pairs separated by newlines)
      const lines = inputData.trim().split('\n')
      const parsedData: DataPoint[] = []
      
      for (const line of lines) {
        const [label, valueStr] = line.split(',').map(item => item.trim())
        const value = parseFloat(valueStr)
        
        if (!label || isNaN(value)) {
          throw new Error(Invalid data format on line: ${line})
        }
        
        parsedData.push({ label, value })
      }
      
      if (parsedData.length === 0) {
        throw new Error('No valid data provided')
      }
      
      setChartData(parsedData)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Invalid data format')
      setChartData([])
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputData(e.target.value)
  }

  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputData(e.target.value)
  }

  const maxValue = Math.max(...chartData.map(item => item.value), 0)
  const totalValue = chartData.reduce((sum, item) => sum + item.value, 0)

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle className="text-2xl font-bold">Bar Chart Generator</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div>
            <Label htmlFor="data-input">Input Data (CSV format)</Label>
            <div className="text-sm text-muted-foreground mb-2">
              Enter data as label,value pairs separated by newlines. Example:
              <pre className="bg-gray-100 p-2 rounded mt-1">Apples,50\nOranges,30\nBananas,20</pre>
            </div>
            <textarea
              id="data-input"
              className="w-full h-32 p-2 border rounded"
              value={inputData}
              onChange={handleTextareaChange}
              placeholder="Enter your data here..."
            />
            {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
            <Button className="mt-2" onClick={parseInputData}>
              Generate Chart
            </Button>
          </div>

          {chartData.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold mb-4">Bar Chart</h3>
              <div className="border rounded-lg p-4 bg-white">
                <div className="flex items-end h-64 gap-2 md:gap-4">
                  {chartData.map((item, index) => (
                    <div key={index} className="flex-1 flex flex-col items-center">
                      <div
                        className="w-full bg-blue-500 rounded-t hover:bg-blue-600 transition-colors"
                        style={{
                          height: ${(item.value / maxValue) * 100}%,
                          minHeight: '1px' // Ensure very small values are visible
                        }}
                        title={${item.label}: ${item.value} (${Math.round((item.value / totalValue) * 100)}%)}
                      />
                      <div className="text-xs mt-2 text-center break-words w-full">
                        {item.label}
                    </div>
                     </div>
                  ))}
                </div>
                <div className="mt-4 text-sm text-gray-500">
                  <p>Total: {totalValue}</p>
                  <p>Max value: {maxValue}</p>
                </div>
              </div>
             </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
