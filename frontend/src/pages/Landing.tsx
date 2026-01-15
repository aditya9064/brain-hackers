import { Link } from 'react-router-dom';

export default function Landing() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center">
            <h1 className="text-2xl font-bold text-primary-700">NeuroVision AI</h1>
          </div>
          <div className="flex items-center space-x-4">
            <Link to="/login" className="text-gray-700 hover:text-primary-700 font-medium">
              Login
            </Link>
            <Link to="/register" className="btn-primary">
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center">
          <h2 className="text-5xl font-bold text-gray-900 mb-6">
            AI-Assisted MRI Analysis for Neurological Conditions
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Advanced brain MRI visualization and analysis platform designed for neurologists and radiologists. 
            Streamline diagnosis workflows with intelligent pattern recognition and comprehensive reporting.
          </p>
          <div className="flex items-center justify-center space-x-4">
            <Link to="/upload" className="btn-primary text-lg px-8 py-4">
              Upload Scan
            </Link>
            <Link to="/viewer" className="btn-secondary text-lg px-8 py-4">
              View Demo
            </Link>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-gray-50 py-20">
        <div className="max-w-7xl mx-auto px-6">
          <h3 className="text-3xl font-bold text-gray-900 text-center mb-12">
            How NeuroVision AI Works
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary-700">1</span>
              </div>
              <h4 className="text-xl font-semibold text-gray-900 mb-2">Upload</h4>
              <p className="text-gray-600">
                Securely upload DICOM or NIfTI format brain MRI scans through our encrypted interface.
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary-700">2</span>
              </div>
              <h4 className="text-xl font-semibold text-gray-900 mb-2">Process</h4>
              <p className="text-gray-600">
                Advanced AI algorithms analyze brain structures, volumes, and identify potential abnormalities.
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary-700">3</span>
              </div>
              <h4 className="text-xl font-semibold text-gray-900 mb-2">Visualize</h4>
              <p className="text-gray-600">
                Interactive 3D brain visualization with multi-planar views and highlighted regions of interest.
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary-700">4</span>
              </div>
              <h4 className="text-xl font-semibold text-gray-900 mb-2">Assist Diagnosis</h4>
              <p className="text-gray-600">
                Comprehensive analysis reports with risk assessments and clinical decision support insights.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Compliance Notice */}
      <section className="bg-primary-50 border-t border-primary-200 py-12">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-gray-700 font-medium">
            For clinical decision support only. Not a replacement for professional medical judgment.
          </p>
          <p className="text-sm text-gray-600 mt-2">
            All predictions and analyses should be reviewed by qualified clinicians before making diagnostic decisions.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 py-12">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h4 className="text-white font-semibold mb-4">NeuroVision AI</h4>
              <p className="text-sm">
                Advanced medical imaging analysis platform for neurological conditions.
              </p>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Resources</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white">Documentation</a></li>
                <li><a href="#" className="hover:text-white">API Reference</a></li>
                <li><a href="#" className="hover:text-white">Support</a></li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-white">Terms of Service</a></li>
                <li><a href="#" className="hover:text-white">HIPAA Compliance</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm">
            <p>&copy; 2024 NeuroVision AI. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
