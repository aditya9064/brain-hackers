// Type definitions for NeuroVision AI application

export interface User {
  id: string;
  name: string;
  email: string;
  role: 'neurologist' | 'radiologist' | 'admin';
  institution: string;
}

export interface MRIScan {
  id: string;
  patientId: string;
  patientName: string;
  uploadDate: string;
  scanType: 'T1' | 'T2' | 'FLAIR' | 'DWI';
  status: 'uploaded' | 'processing' | 'completed' | 'error';
  fileSize: number;
  fileName: string;
}

export interface AnalysisResult {
  scanId: string;
  riskScores: {
    alzheimers: number;
    mci: number;
    normal: number;
  };
  confidence: number;
  findings: Finding[];
  regions: RegionAnalysis[];
  comparisonBaseline: BaselineComparison;
}

export interface Finding {
  id: string;
  region: string;
  severity: 'mild' | 'moderate' | 'severe';
  description: string;
  confidence: number;
}

export interface RegionAnalysis {
  region: string;
  volume: number;
  normalVolume: number;
  deviation: number;
  status: 'normal' | 'atrophy' | 'enlarged';
}

export interface BaselineComparison {
  ageMatched: boolean;
  populationAverage: number;
  patientValue: number;
  percentile: number;
}

export interface Patient {
  id: string;
  name: string;
  age: number;
  sex: 'M' | 'F';
  scanHistory: MRIScan[];
}
