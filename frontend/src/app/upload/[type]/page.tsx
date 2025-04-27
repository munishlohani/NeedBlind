'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { use } from 'react';
import Nav from '@/components/Nav';
import ImageUploadSection from '@/components/ImageUploadSection';
import ChatPopup from '@/components/ChatPopup';
import { IoMdArrowBack } from "react-icons/io";


export default function UploadPage({ params }: { params: Promise<{ type: string }> }) {
  const router = useRouter();
  const [showChat, setShowChat] = useState(false);
  const resolvedParams = use(params);

  const getTitle = () => {
    switch (resolvedParams.type) {
      case 'tuberculosis':
        return 'Tuberculosis Analysis';
      case 'pneumonia':
        return 'Pneumonia Analysis';
      case 'brain_tumor':
        return 'Brain Tumor Analysis';
      case 'skin_diseases':
        return "Skin Disease Analysis"
      case 'knee':
        return "Knee Osteoarthritis Analysis"
      default:
        return 'Medical Image Analysis';
    }
  };

  return (
    <>
      <Nav />
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto">
        <button
              onClick={() => router.back()}
              className="mr-4 text-gray-600 hover:text-purple-800"
            >
              <span className='cursor-pointer'>
                <IoMdArrowBack />
                Back
              </span>
            </button>
          <div className="flex items-center content-center justify-center mb-6">
            
            <h1 className="text-2xl font-bold">{getTitle()}</h1>
          </div>
          
          <div className="bg-white rounded-lg shadow-lg p-6">
            <ImageUploadSection analysisType={resolvedParams.type}/>
          </div>

          <button
            onClick={() => setShowChat(true)}
            className="fixed bottom-6 right-6 cursor-pointer bg-purple-700 text-white px-6 py-3 rounded-full shadow-lg hover:bg-purple-600 transition-colors duration-300"
          >
            Chat with CC
          </button>

          <ChatPopup isOpen={showChat} onClose={() => setShowChat(false)} />
        </div>
      </div>
    </>
  );
} 