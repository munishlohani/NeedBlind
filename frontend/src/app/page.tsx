'use client';

import { useRouter } from 'next/navigation';
import Nav from '@/components/Nav';
import Image from 'next/image';
import tb from '../assets/tb.jpg'
import pneo from '../assets/pneo.jpg'
import tumor from '../assets/tumor.jpg'
import ChatPopup from '@/components/ChatPopup';
import { useState } from 'react';

export default function Home() {
  const router = useRouter();
  const [showChat, setShowChat] = useState(false);

  const uploadOptions = [
    {
      title: 'Upload Tuberclosis',
      description: 'Upload and analyze Tuberclosis',
      icon: tb,
      path: '/upload/tuberculosis'
    },
    {
      title: 'Upload Pneumonia',
      description: 'Upload and analyze Pneumonia',
      icon: pneo,
      path: '/upload/pneumonia'
    },
    {
      title: 'Upload Brain Tumor',
      description: 'Upload and analyze Brain Tumor',
      icon: tumor,
      path: '/upload/brain_tumor'
    }
  ];

  return (
    <>
      <Nav />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-center mb-8 text-purple-700">Medical Image Analysis</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {uploadOptions.map((option, index) => (
            <div
              key={index}
              onClick={() => router.push(option.path)}
              className="bg-white rounded-lg shadow-lg shadow-purple-200 p-6 cursor-pointer hover:shadow-xl transition-shadow duration-300"
            >
              <div className="text-4xl mb-4 flex justify-center items-center ">
                <Image src={option.icon} alt={option.title} className='select-none' />
              </div>
              <h2 className="text-xl font-semibold mb-2">{option.title}</h2>
              <p className="text-gray-600">{option.description}</p>
            </div>
          ))}
        </div>
        <button
          onClick={() => setShowChat(true)}
          className="fixed bottom-6 right-6 cursor-pointer bg-purple-700 text-white px-6 py-3 rounded-full shadow-lg hover:bg-purple-600 transition-colors duration-300"
        >
          Chat with CC
        </button>
        <ChatPopup isOpen={showChat} onClose={() => setShowChat(false)} />
      </div>
    </>
  );
} 