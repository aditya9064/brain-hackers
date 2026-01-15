# NeuroVision AI

A professional medical web application for neurologists and radiologists to analyze brain MRI scans with AI-assisted visualization and analysis.

## Features

- **Secure File Upload**: Drag-and-drop interface for DICOM and NIfTI format MRI files
- **3D Brain Visualization**: Interactive Three.js-based 3D brain viewer with multi-planar slice views
- **AI Analysis**: Risk assessment and regional findings for neurological conditions
- **Patient History**: Comprehensive tracking of past scans and analysis results
- **Clinical Decision Support**: Professional-grade interface designed for healthcare professionals

## Tech Stack

- **React 19** with TypeScript
- **Vite** for build tooling
- **Tailwind CSS** for styling
- **Three.js** for 3D visualization
- **React Router** for navigation

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Open your browser to `http://localhost:5173`

### Build for Production

```bash
npm run build
```

The production build will be in the `dist` directory.

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Layout/         # Sidebar, Header, MainLayout
│   └── MRIViewer/      # 3D visualization components
├── pages/              # Page components
│   ├── Landing.tsx
│   ├── Login.tsx
│   ├── Register.tsx
│   ├── Dashboard.tsx
│   ├── UploadMRI.tsx
│   ├── MRIViewer.tsx
│   ├── AnalysisResults.tsx
│   ├── PatientHistory.tsx
│   └── Settings.tsx
├── types/              # TypeScript type definitions
├── data/               # Mock data for development
└── App.tsx            # Main app component with routing
```

## Design System

### Colors
- Primary: Deep blue (#0369a1)
- Teal: Muted teal for accents
- Gray: Professional gray scale
- Status colors: Red (high risk), Yellow (moderate), Green (normal)

### Typography
- Font: Inter (Google Fonts)
- Clean, sans-serif throughout

## Pages

1. **Landing Page**: Product overview and value proposition
2. **Authentication**: Login, Register, Forgot Password
3. **Dashboard**: Overview of scans and quick actions
4. **Upload MRI**: Secure file upload with drag-and-drop
5. **MRI Viewer**: 3D visualization and 2D slice viewers
6. **Analysis Results**: Risk scores, findings, and regional analysis
7. **Patient History**: Table view of past scans
8. **Settings**: Profile, security, and privacy settings

## Important Notes

- **Clinical Decision Support Only**: All AI-generated analyses are for decision support purposes only
- **HIPAA Compliance**: Designed with healthcare data privacy in mind
- **Mock Data**: Currently uses mock data - ready for backend API integration

## Development

The application uses mock data for development. To connect to a backend API:

1. Update API endpoints in service files (to be created)
2. Replace mock data imports with API calls
3. Add authentication token management
4. Implement real file upload handling

## License

Proprietary - For medical use only
