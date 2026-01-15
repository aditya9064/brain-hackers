// Mock data for development and testing

import type { MRIScan, AnalysisResult, Patient, User } from '../types';

export const mockUser: User = {
  id: '1',
  name: 'Dr. Sarah Chen',
  email: 'sarah.chen@hospital.com',
  role: 'neurologist',
  institution: 'Metropolitan Medical Center',
};

export const mockScans: MRIScan[] = [
  {
    id: '1',
    patientId: 'P001',
    patientName: 'John Doe',
    uploadDate: '2024-01-15T10:30:00Z',
    scanType: 'T1',
    status: 'completed',
    fileSize: 52428800,
    fileName: 'scan_001.nii.gz',
  },
  {
    id: '2',
    patientId: 'P002',
    patientName: 'Jane Smith',
    uploadDate: '2024-01-14T14:20:00Z',
    scanType: 'FLAIR',
    status: 'completed',
    fileSize: 48234496,
    fileName: 'scan_002.nii.gz',
  },
  {
    id: '3',
    patientId: 'P003',
    patientName: 'Robert Johnson',
    uploadDate: '2024-01-13T09:15:00Z',
    scanType: 'T1',
    status: 'processing',
    fileSize: 51200000,
    fileName: 'scan_003.nii.gz',
  },
];

export const mockAnalysisResult: AnalysisResult = {
  scanId: '1',
  riskScores: {
    alzheimers: 68,
    mci: 22,
    normal: 10,
  },
  confidence: 0.87,
  findings: [
    {
      id: 'f1',
      region: 'Hippocampus',
      severity: 'moderate',
      description: 'Bilateral hippocampal volume reduction observed',
      confidence: 0.85,
    },
    {
      id: 'f2',
      region: 'Temporal Lobe',
      severity: 'mild',
      description: 'Slight temporal lobe atrophy',
      confidence: 0.72,
    },
  ],
  regions: [
    {
      region: 'Hippocampus',
      volume: 2.8,
      normalVolume: 3.5,
      deviation: -20,
      status: 'atrophy',
    },
    {
      region: 'Ventricles',
      volume: 45.2,
      normalVolume: 38.0,
      deviation: 19,
      status: 'enlarged',
    },
  ],
  comparisonBaseline: {
    ageMatched: true,
    populationAverage: 3.2,
    patientValue: 2.8,
    percentile: 15,
  },
};

export const mockPatients: Patient[] = [
  {
    id: 'P001',
    name: 'John Doe',
    age: 72,
    sex: 'M',
    scanHistory: [mockScans[0]],
  },
  {
    id: 'P002',
    name: 'Jane Smith',
    age: 68,
    sex: 'F',
    scanHistory: [mockScans[1]],
  },
  {
    id: 'P003',
    name: 'Robert Johnson',
    age: 75,
    sex: 'M',
    scanHistory: [mockScans[2]],
  },
];
