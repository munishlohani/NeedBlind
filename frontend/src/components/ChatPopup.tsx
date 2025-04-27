'use client';

import { useState, useEffect } from 'react';
import Chat from './Chat';
import { RxCross1 } from "react-icons/rx";
 

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatPopupProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function ChatPopup({ isOpen, onClose }: ChatPopupProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => setIsVisible(true), 10);
    } else {
      setIsVisible(false);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50">
      <div 
        className={`absolute inset-0 bg-black/50 backdrop-blur-sm transition-opacity duration-300 ${
          isVisible ? 'opacity-100' : 'opacity-0'
        }`}
        onClick={onClose}
      />
      <div 
        className={`bg-white rounded-lg shadow-xl w-[800px] h-[600px] p-4 transition-all duration-300 transform ${
          isVisible ? 'opacity-100 scale-100 translate-y-0' : 'opacity-0 scale-95 translate-y-10'
        }`}
      >
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Chat with CC</h2>
          <div
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 transition-colors"
          >
            <RxCross1 className="w-6 h-6 cursor-pointer" />
          </div>
        </div>
        <Chat 
          messages={messages} 
          setMessages={setMessages} 
          className="h-[500px]"
        />
      </div>
    </div>
  );
} 