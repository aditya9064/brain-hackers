import { mockAnalysisResult } from '../data/mockData';
import { Link } from 'react-router-dom';

export default function AnalysisResults() {
  const result = mockAnalysisResult;

  const getRiskColor = (score: number) => {
    if (score >= 60) return 'text-red-700 bg-red-50';
    if (score >= 30) return 'text-yellow-700 bg-yellow-50';
    return 'text-green-700 bg-green-50';
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'severe':
        return 'bg-red-100 text-red-700';
      case 'moderate':
        return 'bg-yellow-100 text-yellow-700';
      case 'mild':
        return 'bg-blue-100 text-blue-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Analysis Results</h1>
        <p className="text-gray-600 mt-1">AI-generated analysis and risk assessment</p>
      </div>

      {/* Risk Score Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900">Alzheimer's Risk</h3>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(result.riskScores.alzheimers)}`}>
              {result.riskScores.alzheimers}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-red-600 h-2 rounded-full"
              style={{ width: `${result.riskScores.alzheimers}%` }}
            />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900">MCI Risk</h3>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(result.riskScores.mci)}`}>
              {result.riskScores.mci}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-yellow-600 h-2 rounded-full"
              style={{ width: `${result.riskScores.mci}%` }}
            />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900">Normal</h3>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getRiskColor(result.riskScores.normal)}`}>
              {result.riskScores.normal}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-green-600 h-2 rounded-full"
              style={{ width: `${result.riskScores.normal}%` }}
            />
          </div>
        </div>
      </div>

      {/* Confidence Disclaimer */}
      <div className="card bg-yellow-50 border-yellow-200">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <span className="text-yellow-700 font-semibold">!</span>
          </div>
          <div className="ml-3">
            <h4 className="text-sm font-semibold text-yellow-900">Confidence Level: {(result.confidence * 100).toFixed(0)}%</h4>
            <p className="mt-1 text-sm text-yellow-700">
              This analysis is for clinical decision support only. The confidence score indicates the reliability 
              of the AI assessment. All findings should be reviewed and validated by qualified medical professionals 
              before making diagnostic decisions.
            </p>
          </div>
        </div>
      </div>

      {/* Findings */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Regional Findings</h3>
        <div className="space-y-3">
          {result.findings.map((finding) => (
            <div key={finding.id} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-medium text-gray-900">{finding.region}</h4>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${getSeverityColor(finding.severity)}`}>
                  {finding.severity}
                </span>
              </div>
              <p className="text-sm text-gray-600 mb-2">{finding.description}</p>
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-500">Confidence: {(finding.confidence * 100).toFixed(0)}%</span>
                <Link to="/viewer" className="text-xs text-primary-700 hover:text-primary-800 font-medium">
                  View in 3D →
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Region Analysis */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Volume Analysis</h3>
        <div className="space-y-4">
          {result.regions.map((region, index) => (
            <div key={index}>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">{region.region}</span>
                <span className={`text-xs font-medium ${
                  region.status === 'atrophy' ? 'text-red-700' :
                  region.status === 'enlarged' ? 'text-yellow-700' :
                  'text-green-700'
                }`}>
                  {region.status}
                </span>
              </div>
              <div className="grid grid-cols-3 gap-4 text-sm mb-2">
                <div>
                  <span className="text-gray-500">Volume:</span>
                  <span className="ml-2 font-medium text-gray-900">{region.volume} cm³</span>
                </div>
                <div>
                  <span className="text-gray-500">Normal:</span>
                  <span className="ml-2 font-medium text-gray-900">{region.normalVolume} cm³</span>
                </div>
                <div>
                  <span className="text-gray-500">Deviation:</span>
                  <span className={`ml-2 font-medium ${
                    region.deviation < 0 ? 'text-red-700' : 'text-yellow-700'
                  }`}>
                    {region.deviation > 0 ? '+' : ''}{region.deviation}%
                  </span>
                </div>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className={`h-2 rounded-full ${
                    region.status === 'atrophy' ? 'bg-red-600' :
                    region.status === 'enlarged' ? 'bg-yellow-600' :
                    'bg-green-600'
                  }`}
                  style={{ width: `${Math.abs(region.deviation)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Baseline Comparison */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Baseline Comparison</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <span className="text-sm text-gray-700">Age-matched population average</span>
            <span className="font-medium text-gray-900">{result.comparisonBaseline.populationAverage} cm³</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <span className="text-sm text-gray-700">Patient value</span>
            <span className="font-medium text-gray-900">{result.comparisonBaseline.patientValue} cm³</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-primary-50 rounded-lg">
            <span className="text-sm text-gray-700">Percentile rank</span>
            <span className="font-medium text-primary-700">{result.comparisonBaseline.percentile}th percentile</span>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center justify-end space-x-4">
        <Link to="/viewer" className="btn-secondary">
          View in 3D
        </Link>
        <button className="btn-primary">
          Export Report
        </button>
      </div>
    </div>
  );
}
