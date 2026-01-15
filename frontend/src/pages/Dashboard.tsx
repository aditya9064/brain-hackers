import { Link } from 'react-router-dom';
import { mockScans } from '../data/mockData';

export default function Dashboard() {
  const recentScans = mockScans.slice(0, 3);
  const completedScans = mockScans.filter(s => s.status === 'completed').length;
  const processingScans = mockScans.filter(s => s.status === 'processing').length;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">Overview of your MRI analysis activities</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Scans</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{mockScans.length}</p>
            </div>
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
              <span className="text-primary-700 font-semibold">T</span>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Completed</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{completedScans}</p>
            </div>
            <div className="w-12 h-12 bg-teal-100 rounded-lg flex items-center justify-center">
              <span className="text-teal-700 font-semibold">C</span>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Processing</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{processingScans}</p>
            </div>
            <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
              <span className="text-yellow-700 font-semibold">P</span>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <Link to="/upload" className="btn-primary w-full text-center block">
              Upload New MRI Scan
            </Link>
            <Link to="/viewer" className="btn-secondary w-full text-center block">
              Open 3D Viewer
            </Link>
            <Link to="/history" className="btn-secondary w-full text-center block">
              View Patient History
            </Link>
          </div>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Scans</h3>
          <div className="space-y-3">
            {recentScans.map((scan) => (
              <div key={scan.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">{scan.patientName}</p>
                  <p className="text-sm text-gray-600">{scan.scanType} - {new Date(scan.uploadDate).toLocaleDateString()}</p>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                  scan.status === 'completed' ? 'bg-teal-100 text-teal-700' :
                  scan.status === 'processing' ? 'bg-yellow-100 text-yellow-700' :
                  'bg-gray-100 text-gray-700'
                }`}>
                  {scan.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Important Notice */}
      <div className="card bg-primary-50 border-primary-200">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <span className="text-primary-700 font-semibold text-lg">!</span>
          </div>
          <div className="ml-3">
            <h4 className="text-sm font-semibold text-primary-900">Clinical Decision Support Only</h4>
            <p className="mt-1 text-sm text-primary-700">
              All AI-generated analyses are for clinical decision support purposes only. 
              Final diagnostic decisions must be made by qualified medical professionals.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
