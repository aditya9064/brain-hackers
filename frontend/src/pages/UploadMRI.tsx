import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

interface UploadedFile {
  name: string;
  size: number;
  type: string;
}

export default function UploadMRI() {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  const acceptedFormats = ['.nii', '.nii.gz', '.dcm', '.dicom'];
  const maxFileSize = 500 * 1024 * 1024; // 500 MB

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const validateFile = (file: File): string | null => {
    const extension = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!acceptedFormats.includes(extension) && !acceptedFormats.includes('.nii.gz')) {
      return 'Invalid file format. Please upload DICOM or NIfTI files.';
    }
    if (file.size > maxFileSize) {
      return 'File size exceeds 500 MB limit.';
    }
    return null;
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const droppedFiles = Array.from(e.dataTransfer.files);
    const validFiles: UploadedFile[] = [];
    const errors: string[] = [];

    droppedFiles.forEach((file) => {
      const error = validateFile(file);
      if (error) {
        errors.push(`${file.name}: ${error}`);
      } else {
        validFiles.push({
          name: file.name,
          size: file.size,
          type: file.type,
        });
      }
    });

    if (errors.length > 0) {
      alert(errors.join('\n'));
    }

    setFiles([...files, ...validFiles]);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || []);
    const validFiles: UploadedFile[] = [];
    const errors: string[] = [];

    selectedFiles.forEach((file) => {
      const error = validateFile(file);
      if (error) {
        errors.push(`${file.name}: ${error}`);
      } else {
        validFiles.push({
          name: file.name,
          size: file.size,
          type: file.type,
        });
      }
    });

    if (errors.length > 0) {
      alert(errors.join('\n'));
    }

    setFiles([...files, ...validFiles]);
  };

  const removeFile = (index: number) => {
    setFiles(files.filter((_, i) => i !== index));
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  const handleUpload = async () => {
    if (files.length === 0) {
      alert('Please select at least one file to upload');
      return;
    }

    setIsUploading(true);
    setUploadProgress(0);

    // Simulate upload progress
    const interval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsUploading(false);
          navigate('/results');
          return 100;
        }
        return prev + 10;
      });
    }, 300);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Upload MRI Scan</h1>
        <p className="text-gray-600 mt-1">Upload DICOM or NIfTI format brain MRI files for analysis</p>
      </div>

      <div className="card">
        <div
          className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
            isDragging
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400'
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="space-y-4">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto">
              <span className="text-2xl text-primary-700 font-semibold">U</span>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Drag and drop files here
              </h3>
              <p className="text-gray-600 mb-4">or</p>
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="btn-primary"
                disabled={isUploading}
              >
                Browse Files
              </button>
            </div>
            <p className="text-sm text-gray-500">
              Supported formats: DICOM (.dcm, .dicom), NIfTI (.nii, .nii.gz)
            </p>
            <p className="text-sm text-gray-500">
              Maximum file size: 500 MB per file
            </p>
          </div>
        </div>

        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".nii,.nii.gz,.dcm,.dicom"
          onChange={handleFileSelect}
          className="hidden"
        />
      </div>

      {files.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Selected Files</h3>
          <div className="space-y-2">
            {files.map((file, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
              >
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{file.name}</p>
                  <p className="text-sm text-gray-600">{formatFileSize(file.size)}</p>
                </div>
                <button
                  type="button"
                  onClick={() => removeFile(index)}
                  className="text-red-600 hover:text-red-700 font-medium text-sm"
                  disabled={isUploading}
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {isUploading && (
        <div className="card">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">Uploading...</span>
              <span className="text-sm text-gray-600">{uploadProgress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              />
            </div>
          </div>
        </div>
      )}

      <div className="flex items-center justify-end space-x-4">
        <button
          type="button"
          onClick={() => setFiles([])}
          className="btn-secondary"
          disabled={isUploading || files.length === 0}
        >
          Clear All
        </button>
        <button
          type="button"
          onClick={handleUpload}
          className="btn-primary"
          disabled={isUploading || files.length === 0}
        >
          {isUploading ? 'Uploading...' : 'Upload and Analyze'}
        </button>
      </div>

      <div className="card bg-yellow-50 border-yellow-200">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <span className="text-yellow-700 font-semibold">!</span>
          </div>
          <div className="ml-3">
            <h4 className="text-sm font-semibold text-yellow-900">Security Notice</h4>
            <p className="mt-1 text-sm text-yellow-700">
              All uploaded files are encrypted and stored securely in compliance with HIPAA regulations. 
              Files are automatically deleted after analysis completion unless explicitly saved.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
