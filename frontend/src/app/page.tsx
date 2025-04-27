'use client';

import { useRouter } from 'next/navigation';
import Nav from '@/components/Nav';
import Image from 'next/image';
import tb from '../assets/tb.jpg'
import pneo from '../assets/pneo.jpg'
import tumor from '../assets/tumor.jpg'
import skin from "../assets/skin.jpg"
import knee from "../assets/knee.jpg"
import ChatPopup from '@/components/ChatPopup';
import { useState } from 'react';

export default function Home() {
  const router = useRouter();
  const [showChat, setShowChat] = useState(false);

  const uploadOptions = [
    {
      title: 'Upload Tuberculosis',
      description: 'Upload and analyze Tuberculosis',
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
    },
    {
      title: 'Upload Skin Diseases',
      description: 'Upload and analyze Skin Diseases',
      icon: skin,
      path: '/upload/skin_diseases'
    },
    {
      title: 'Upload Knee Osteoarthritis',
      description: 'Upload and analyze Knee Osteoarthritis',
      icon: knee,
      path: '/upload/knee'
    }
  ];

  return (
    <>
      <Nav />
      <div className="container mx-auto px-0 py-8">
        <h1 className="text-3xl font-bold text-center mb-5 text-purple-700 ">DocC- Your Health Companion</h1>
        <div className="flex flex-col lg:flex-row gap-3">
          {uploadOptions.map((option, index) => (
            <div
              key={index}
              onClick={() => router.push(option.path)}
              className="bg-white rounded-lg shadow-lg shadow-purple-200 p-6 cursor-pointer hover:shadow-xl transition-shadow duration-300"
            >
              <div className="text-4xl mb-3 flex justify-center items-center ">
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