import { useState } from 'react';
import { Link } from 'react-router-dom';
import { mockScans, mockPatients } from '../data/mockData';

export default function PatientHistory() {
  const [selectedPatient, setSelectedPatient] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  const filteredScans = mockScans.filter((scan) => {
    const matchesSearch = scan.patientName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         scan.patientId.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesPatient = !selectedPatient || scan.patientId === selectedPatient;
    return matchesSearch && matchesPatient;
  });

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const formatFileSize = (bytes: number) => {
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  const getStatusBadge = (status: string) => {
    const styles = {
      completed: 'bg-teal-100 text-teal-700',
      processing: 'bg-yellow-100 text-yellow-700',
      uploaded: 'bg-blue-100 text-blue-700',
      error: 'bg-red-100 text-red-700',
    };
    return styles[status as keyof typeof styles] || 'bg-gray-100 text-gray-700';
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Patient History</h1>
        <p className="text-gray-600 mt-1">View and manage past MRI scans and analysis results</p>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
              Search
            </label>
            <input
              id="search"
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field"
              placeholder="Search by patient name or ID..."
            />
          </div>
          <div>
            <label htmlFor="patient" className="block text-sm font-medium text-gray-700 mb-2">
              Filter by Patient
            </label>
            <select
              id="patient"
              value={selectedPatient || ''}
              onChange={(e) => setSelectedPatient(e.target.value || null)}
              className="input-field"
            >
              <option value="">All Patients</option>
              {mockPatients.map((patient) => (
                <option key={patient.id} value={patient.id}>
                  {patient.name} ({patient.id})
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Scans Table */}
      <div className="card p-0 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Patient
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Scan Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Upload Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  File Size
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredScans.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-gray-500">
                    No scans found matching your criteria
                  </td>
                </tr>
              ) : (
                filteredScans.map((scan) => (
                  <tr key={scan.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{scan.patientName}</div>
                        <div className="text-sm text-gray-500">{scan.patientId}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-900">{scan.scanType}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-900">{formatDate(scan.uploadDate)}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-900">{formatFileSize(scan.fileSize)}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-3 py-1 inline-flex text-xs leading-5 font-medium rounded-full ${getStatusBadge(scan.status)}`}>
                        {scan.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex items-center space-x-3">
                        {scan.status === 'completed' && (
                          <>
                            <Link
                              to="/results"
                              className="text-primary-700 hover:text-primary-800"
                            >
                              View Results
                            </Link>
                            <Link
                              to="/viewer"
                              className="text-primary-700 hover:text-primary-800"
                            >
                              View 3D
                            </Link>
                          </>
                        )}
                        <button className="text-gray-600 hover:text-gray-800">
                          Download
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <p className="text-sm text-gray-600">Total Scans</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{mockScans.length}</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-600">Completed</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">
            {mockScans.filter(s => s.status === 'completed').length}
          </p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-600">Total Patients</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{mockPatients.length}</p>
        </div>
      </div>
    </div>
  );
}
