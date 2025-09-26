'use client';

import { useState, useEffect, useRef } from 'react';
import { api, checkBackendConnection } from '../lib/api';
import VoiceIndicator from './VoiceIndicator';

interface Message {
  text: string;
  isUser: boolean;
  timestamp: Date;
}

export default function VoiceAssistant() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState<'connecting' | 'connected' | 'disconnected'>('connecting');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Focus input on load
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  useEffect(() => {
    // Get initial greeting and check backend status
    const fetchGreeting = async () => {
      setIsLoading(true);
      
      // Check backend connection
      const isConnected = await checkBackendConnection();
      setBackendStatus(isConnected ? 'connected' : 'disconnected');
      
      try {
        const response = await api.getGreeting();
        
        if (response.message) {
          addMessage({
            text: response.message,
            isUser: false,
            timestamp: new Date()
          });
        }
      } catch (error) {
        console.error('Failed to get greeting:', error);
        addMessage({
          text: 'Welcome to Talksy! I\'m your private voice assistant. The backend server appears to be offline, so I\'ll be operating in limited mode.',
          isUser: false,
          timestamp: new Date()
        });
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchGreeting();
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const addMessage = (message: Message) => {
    setMessages(prev => [...prev, message]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!inputText.trim() || isLoading) return;
    
    // Add user message
    addMessage({
      text: inputText,
      isUser: true,
      timestamp: new Date()
    });
    
    const command = inputText;
    setInputText('');
    setIsLoading(true);
    
    try {
      const response = await api.processTextCommand(command);
      setBackendStatus(response.success === false ? 'disconnected' : 'connected');
      
      // Add assistant response
      if (response.response) {
        addMessage({
          text: response.response,
          isUser: false,
          timestamp: new Date()
        });
      }
    } catch (error) {
      console.error('Error processing command:', error);
      setBackendStatus('disconnected');
      addMessage({
        text: 'Sorry, I encountered an error while processing your request. Please ensure the backend server is running at http://localhost:8000.',
        isUser: false,
        timestamp: new Date()
      });
    } finally {
      setIsLoading(false);
      
      // Re-focus the input
      if (inputRef.current) {
        inputRef.current.focus();
      }
    }
  };

  const toggleListening = async () => {
    if (isListening) {
      setIsListening(false);
      return;
    }
    
    // Don't try to listen if backend is disconnected
    if (backendStatus === 'disconnected') {
      addMessage({
        text: 'Voice recognition requires the backend server to be running. Please start the backend server and try again.',
        isUser: false,
        timestamp: new Date()
      });
      return;
    }
    
    setIsListening(true);
    setIsLoading(true);
    
    try {
      const response = await api.listenForCommand();
      setBackendStatus(response.success === false ? 'disconnected' : 'connected');
      
      if (response.success && response.command) {
        // Add user's spoken command
        addMessage({
          text: response.command,
          isUser: true,
          timestamp: new Date()
        });
        
        // Add assistant's response
        if (response.response) {
          addMessage({
            text: response.response,
            isUser: false,
            timestamp: new Date()
          });
        }
      } else {
        // If there was an error or no command detected
        addMessage({
          text: response.command || "I couldn't hear what you said. Please try again.",
          isUser: false,
          timestamp: new Date()
        });
      }
    } catch (error) {
      console.error('Error listening for command:', error);
      setBackendStatus('disconnected');
      addMessage({
        text: 'Sorry, I encountered an error while trying to listen. Please ensure the backend server is running at http://localhost:8000.',
        isUser: false,
        timestamp: new Date()
      });
    } finally {
      setIsListening(false);
      setIsLoading(false);
      
      // Re-focus the input
      if (inputRef.current) {
        inputRef.current.focus();
      }
    }
  };

  return (
    <div className="flex flex-col h-screen max-h-screen pt-16 pb-16">
      {/* Backend Status Indicator */}
      {backendStatus !== 'connected' && (
        <div className="bg-amber-50 border-y border-amber-200 text-amber-800 dark:bg-amber-900/30 dark:border-amber-900/50 dark:text-amber-200 px-4 py-2 text-sm flex items-center justify-center">
          {backendStatus === 'connecting' 
            ? 'Connecting to backend server...' 
            : 'Backend server not connected. Voice recognition will be unavailable.'}
        </div>
      )}
      
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg px-4 py-2 ${
                message.isUser
                  ? 'bg-blue-500 text-white'
                  : 'bg-[var(--color-foreground-muted)] bg-opacity-10 text-[var(--color-foreground)]'
              }`}
            >
              <p>{message.text}</p>
              <p className="text-xs opacity-70 text-right mt-1">
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </p>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-[var(--color-foreground-muted)] bg-[var(--color-background)] p-4">
        {isListening && (
          <div className="mb-4 flex justify-center items-center">
            <VoiceIndicator isActive={isListening} />
            <p className="ml-2 text-sm text-blue-500 animate-pulse">Listening...</p>
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="flex items-center space-x-2">
          <button
            type="button"
            onClick={toggleListening}
            disabled={(isLoading && !isListening) || backendStatus === 'connecting'}
            aria-label={isListening ? 'Stop listening' : 'Start listening'}
            className={`p-3 rounded-full transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${
              isListening
                ? 'bg-red-500 text-white animate-pulse'
                : backendStatus === 'disconnected'
                  ? 'bg-gray-300 text-gray-600 dark:bg-gray-700 dark:text-gray-400'
                  : 'bg-blue-500 text-white hover:bg-blue-600'
            }`}
          >
            <MicrophoneIcon isActive={isListening && !isLoading} />
          </button>
          
          <input
            ref={inputRef}
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            disabled={isLoading || isListening}
            placeholder={backendStatus === 'disconnected' ? "Limited functionality without backend..." : "Type a message..."}
            className="flex-1 rounded-full border border-[var(--color-foreground-muted)] bg-[var(--color-background)] px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          />
          
          <button
            type="submit"
            disabled={!inputText.trim() || isLoading || isListening}
            aria-label="Send message"
            className="p-3 rounded-full bg-blue-500 text-white hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <SendIcon />
          </button>
        </form>
        
        {isLoading && !isListening && (
          <div className="text-center text-sm text-[var(--color-foreground-muted)] mt-2 animate-pulse">
            Processing...
          </div>
        )}
      </div>
    </div>
  );
}

function MicrophoneIcon({ isActive }: { isActive: boolean }) {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path 
        d="M12 14C13.66 14 15 12.66 15 11V5C15 3.34 13.66 2 12 2C10.34 2 9 3.34 9 5V11C9 12.66 10.34 14 12 14Z" 
        fill="currentColor" 
      />
      <path 
        d="M17.91 11C17.91 11.41 17.87 11.8 17.82 12.18C17.71 12.9 18.23 13.56 18.95 13.67C19.04 13.69 19.12 13.7 19.2 13.7C19.83 13.7 20.4 13.25 20.5 12.61C20.56 12.09 20.59 11.56 20.59 11C20.59 5.93 16.65 1.86 11.63 1.77C11.37 1.77 11.15 1.95 11.1 2.2C11.04 2.46 11.21 2.71 11.47 2.77C15.77 3.55 18.91 6.95 18.91 11H17.91Z" 
        fill="currentColor" 
      />
      <path 
        d="M12 16.55C8.08 16.55 4.92 13.39 4.92 9.47C4.92 9.23 4.93 8.97 4.96 8.7C4.99 8.44 4.83 8.18 4.58 8.11C4.32 8.04 4.06 8.19 3.99 8.45C3.94 8.78 3.92 9.12 3.92 9.47C3.92 13.95 7.52 17.55 12 17.55C12.45 17.55 12.89 17.5 13.32 17.42C13.58 17.37 13.76 17.13 13.72 16.87C13.67 16.61 13.42 16.42 13.16 16.47C12.78 16.52 12.39 16.55 12 16.55Z" 
        fill="currentColor" 
      />
      {!isActive && (
        <path 
          d="M19.51 5.51L18.35 6.67C19.6 7.91 20.34 9.61 20.34 11.47C20.34 11.56 20.34 11.65 20.34 11.74C20.32 12 20.53 12.22 20.78 12.25H20.83C21.07 12.25 21.27 12.07 21.29 11.83C21.3 11.71 21.3 11.59 21.3 11.47C21.3 9.33 20.45 7.38 19 5.93L17.84 7.09C18.94 8.2 19.6 9.76 19.6 11.47C19.6 11.83 19.57 12.19 19.5 12.54C19.44 12.8 19.61 13.05 19.87 13.11C19.91 13.12 19.95 13.12 19.98 13.12C20.21 13.12 20.41 12.96 20.46 12.73C20.54 12.32 20.58 11.9 20.58 11.47C20.58 9.47 19.8 7.63 18.51 6.33L19.51 5.51Z" 
          fill="currentColor" 
        />
      )}
      <path 
        d="M12 19.97C11.25 19.97 10.5 19.87 9.8 19.67C9.54 19.59 9.28 19.75 9.21 20.01C9.13 20.27 9.28 20.55 9.54 20.62C10.35 20.85 11.17 20.97 12 20.97C12.83 20.97 13.65 20.86 14.46 20.62C14.72 20.54 14.88 20.27 14.8 20.01C14.72 19.75 14.46 19.58 14.2 19.67C13.5 19.87 12.76 19.97 12 19.97Z" 
        fill="currentColor" 
      />
      <path 
        d="M12 22C11.59 22 11.25 22.34 11.25 22.75C11.25 23.16 11.59 23.5 12 23.5C12.41 23.5 12.75 23.16 12.75 22.75C12.75 22.34 12.41 22 12 22Z" 
        fill="currentColor" 
      />
    </svg>
  );
}

function SendIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path 
        d="M16.14 2.96L7.11 5.96C1.04 7.99 1.04 11.3 7.11 13.32L9.79 14.21L10.68 16.89C12.7 22.96 16.02 22.96 18.04 16.89L21.05 7.87C22.39 3.82 20.19 1.61 16.14 2.96ZM16.46 8.34L12.66 12.16C12.51 12.31 12.32 12.38 12.13 12.38C11.94 12.38 11.75 12.31 11.6 12.16C11.31 11.87 11.31 11.39 11.6 11.1L15.4 7.28C15.69 6.99 16.17 6.99 16.46 7.28C16.75 7.57 16.75 8.05 16.46 8.34Z" 
        fill="currentColor" 
      />
    </svg>
  );
} 