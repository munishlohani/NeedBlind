'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

interface ImageUploadSectionProps {
  analysisType: string;
}

export default function ImageUploadSection({ analysisType }: ImageUploadSectionProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [result, setResult] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setUploadedFile(file);
      const reader = new FileReader();
      reader.onload = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.dicom']
    },
    maxFiles: 1
  });

  const handleAnalyze = async () => {
    if (!uploadedFile) return;

    setIsLoading(true);
    setResult(null);
    const formData = new FormData();
    formData.append('image', uploadedFile);
    formData.append('type', analysisType);

    try {
      const response = await axios.post('http://localhost:5000/analyze-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data.analysis);
    } catch (error) {
      console.error('Error analyzing image:', error);
      if (axios.isAxiosError(error)) {
        if (error.response) {

          setResult(`Error: ${error.response.data.error || 'Server error'}`);
        } else if (error.request) {
          setResult('Error: No response from server. Please check if the backend is running.');
        } else {
          setResult(`Error: ${error.message}`);
        }
      } else {
        setResult('Failed to analyze image. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full space-y-4">
    

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-purple-500 bg-blue-50' : 'border-gray-300 hover:border-purple-400'}`}
      >
        <input {...getInputProps()} />
        {preview ? (
          <div className="space-y-4">
            <img
              src={preview}
              alt="Preview"
              className="max-h-64 mx-auto rounded-lg shadow-md"
            />
            <button
              onClick={(e) => {
                e.stopPropagation();
                handleAnalyze();
              }}
              disabled={isLoading}
              className={`px-4 py-2 rounded-lg text-white
                ${isLoading ? 'bg-gray-400' : 'bg-purple-700 hover:bg-purple-600'}
                transition-colors`}
            >
              {isLoading ? 'Analyzing...' : 'Analyze Image'}
            </button>
          </div>
        ) : (
          <div className="space-y-2">
            <p className="text-lg text-gray-600">
              {isDragActive
                ? 'Drop the image here'
                : 'Drag and drop an image here, or click to select'}
            </p>
            <p className="text-sm text-gray-500">
              Supports JPG and PNG formats
            </p>
          </div>
        )}
      </div>

      {result && (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
          <h3 className="font-semibold mb-2">Analysis Results:</h3>
          <p className="text-gray-700">{result}</p>
        </div>
      )}
    </div>
  );
} 