import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './components/Layout/MainLayout';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';
import Dashboard from './pages/Dashboard';
import UploadMRI from './pages/UploadMRI';
import MRIViewer from './pages/MRIViewer';
import AnalysisResults from './pages/AnalysisResults';
import PatientHistory from './pages/PatientHistory';
import Settings from './pages/Settings';

function App() {
  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />

        {/* Protected routes with layout */}
        <Route element={<MainLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/upload" element={<UploadMRI />} />
          <Route path="/viewer" element={<MRIViewer />} />
          <Route path="/results" element={<AnalysisResults />} />
          <Route path="/history" element={<PatientHistory />} />
          <Route path="/settings" element={<Settings />} />
        </Route>

        {/* Default redirect */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
