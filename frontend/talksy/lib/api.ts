// API service for connecting to the FastAPI backend

export interface ApiResponse {
  success?: boolean;
  message?: string;
  response?: string;
  command?: string;
  spoken?: string;
  text?: string;
}

const API_URL = 'http://localhost:8000';

// Default fallback responses when backend is unavailable
const FALLBACK_RESPONSES = {
  greeting: "Welcome to Talksy! I'm your offline voice assistant. The backend server is not connected, so I'm working in limited mode.",
  unknown: "I'm sorry, I can't process that right now. The backend server might be offline."
};

/**
 * Makes an API call to the backend
 */
async function fetchApi(endpoint: string, options?: RequestInit): Promise<Response> {
  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });
    return response;
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    throw error;
  }
}

/**
 * Checks if the backend is accessible
 */
export async function checkBackendConnection(): Promise<boolean> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3000);
    
    const response = await fetch(`${API_URL}`, { 
      signal: controller.signal 
    });
    
    clearTimeout(timeoutId);
    return response.ok;
  } catch (error) {
    console.error('Backend connection error:', error);
    return false;
  }
}

export const api = {
  /**
   * Gets a greeting from the assistant
   */
  async getGreeting(): Promise<ApiResponse> {
    try {
      // Check if backend is available
      const isConnected = await checkBackendConnection();
      if (!isConnected) {
        return { 
          success: false, 
          message: FALLBACK_RESPONSES.greeting 
        };
      }
      
      const response = await fetchApi('/greet');
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error getting greeting:', error);
      return { 
        success: false, 
        message: FALLBACK_RESPONSES.greeting 
      };
    }
  },

  /**
   * Processes a text command
   */
  async processTextCommand(command: string): Promise<ApiResponse> {
    try {
      // Check if backend is available
      const isConnected = await checkBackendConnection();
      if (!isConnected) {
        return { 
          success: false, 
          response: `${FALLBACK_RESPONSES.unknown} I received: "${command}"` 
        };
      }
      
      const response = await fetchApi('/process-text', {
        method: 'POST',
        body: JSON.stringify({ command }),
      });
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error processing command:', error);
      return { 
        success: false, 
        response: 'Failed to process your command. Is the backend server running?' 
      };
    }
  },

  /**
   * Makes the assistant listen for voice commands
   */
  async listenForCommand(): Promise<ApiResponse> {
    try {
      // Check if backend is available
      const isConnected = await checkBackendConnection();
      if (!isConnected) {
        return { 
          success: false, 
          command: "Voice recognition requires the backend server to be running."
        };
      }
      
      const response = await fetchApi('/listen', {
        method: 'POST',
      });
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error listening for command:', error);
      return { 
        success: false, 
        command: 'Failed to listen for command. Is the backend server running?' 
      };
    }
  },

  /**
   * Makes the assistant speak text
   */
  async speak(text: string): Promise<ApiResponse> {
    try {
      // Check if backend is available
      const isConnected = await checkBackendConnection();
      if (!isConnected) {
        return { 
          success: false, 
          text: 'Text-to-speech requires the backend server to be running.' 
        };
      }
      
      const response = await fetchApi('/speak', {
        method: 'POST',
        body: JSON.stringify({ text }),
      });
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error making assistant speak:', error);
      return { 
        success: false, 
        text: 'Failed to speak. Is the backend server running?' 
      };
    }
  }
}; 