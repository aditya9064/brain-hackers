import { useState } from 'react';
import Viewer3D from '../components/MRIViewer/Viewer3D';

export default function MRIViewer() {
  const [activeView, setActiveView] = useState<'axial' | 'coronal' | 'sagittal'>('axial');
  const [sliceIndex, setSliceIndex] = useState(50);
  const [opacity, setOpacity] = useState(100);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">MRI Viewer</h1>
        <p className="text-gray-600 mt-1">Interactive 3D brain visualization and multi-planar slice viewing</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* 3D Viewer */}
        <div className="lg:col-span-2 card p-0 overflow-hidden">
          <div className="p-4 border-b border-gray-200">
            <h3 className="font-semibold text-gray-900">3D Brain Visualization</h3>
          </div>
          <div className="h-[600px] relative">
            <Viewer3D />
          </div>
        </div>

        {/* Controls */}
        <div className="space-y-6">
          {/* View Selection */}
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">View Orientation</h3>
            <div className="space-y-2">
              {(['axial', 'coronal', 'sagittal'] as const).map((view) => (
                <button
                  key={view}
                  onClick={() => setActiveView(view)}
                  className={`w-full px-4 py-3 rounded-lg text-left transition-colors ${
                    activeView === view
                      ? 'bg-primary-50 text-primary-700 font-medium'
                      : 'bg-gray-50 text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  {view.charAt(0).toUpperCase() + view.slice(1)} View
                </button>
              ))}
            </div>
          </div>

          {/* Slice Navigation */}
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">Slice Navigation</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-700 mb-2">
                  Slice: {sliceIndex} / 100
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={sliceIndex}
                  onChange={(e) => setSliceIndex(Number(e.target.value))}
                  className="w-full"
                />
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => setSliceIndex(Math.max(0, sliceIndex - 1))}
                  className="btn-secondary flex-1"
                >
                  Previous
                </button>
                <button
                  onClick={() => setSliceIndex(Math.min(100, sliceIndex + 1))}
                  className="btn-secondary flex-1"
                >
                  Next
                </button>
              </div>
            </div>
          </div>

          {/* Opacity Control */}
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">Opacity</h3>
            <div>
              <label className="block text-sm text-gray-700 mb-2">
                {opacity}%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={opacity}
                onChange={(e) => setOpacity(Number(e.target.value))}
                className="w-full"
              />
            </div>
          </div>

          {/* Highlighted Regions */}
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">Abnormal Regions</h3>
            <div className="space-y-2">
              <div className="flex items-center justify-between p-2 bg-red-50 rounded">
                <span className="text-sm text-gray-700">Hippocampus</span>
                <span className="text-xs text-red-700 font-medium">Atrophy</span>
              </div>
              <div className="flex items-center justify-between p-2 bg-yellow-50 rounded">
                <span className="text-sm text-gray-700">Temporal Lobe</span>
                <span className="text-xs text-yellow-700 font-medium">Mild</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 2D Slice Viewers */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {(['axial', 'coronal', 'sagittal'] as const).map((view) => (
          <div key={view} className="card">
            <h3 className="font-semibold text-gray-900 mb-4">
              {view.charAt(0).toUpperCase() + view.slice(1)} Slice
            </h3>
            <div className="bg-gray-100 rounded-lg h-64 flex items-center justify-center">
              <div className="text-center">
                <div className="w-32 h-32 bg-gray-300 rounded-lg mx-auto mb-2"></div>
                <p className="text-sm text-gray-600">Slice {sliceIndex}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
