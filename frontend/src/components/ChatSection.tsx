'use client';

import Chat from './Chat';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatSectionProps {
  messages: Message[];
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
}

export default function ChatSection({ messages, setMessages }: ChatSectionProps) {
  return (
    <Chat 
      messages={messages} 
      setMessages={setMessages} 
      className="h-[600px]"
    />
  );
} 