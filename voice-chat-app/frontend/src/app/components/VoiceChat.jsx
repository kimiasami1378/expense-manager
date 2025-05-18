import { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Send } from 'lucide-react';
import axios from 'axios';

export default function VoiceChat() {
  const [messages, setMessages] = useState([
    { role: 'system', content: 'Hello! Speak or type to start a conversation.' }
  ]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const messagesEndRef = useRef(null);

  // Auto scroll to bottom when messages update
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Start recording audio from microphone
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Create a new MediaRecorder instance
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      // When data is available, add it to our array of audio chunks
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      // When recording stops, process the audio
      mediaRecorder.onstop = () => {
        processAudio();
      };

      // Start recording
      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Could not access microphone. Please check permissions.');
    }
  };

  // Stop recording
  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      
      // Stop all audio tracks
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
  };

  // Process recorded audio
  const processAudio = async () => {
    setIsProcessing(true);
    
    // Create a blob from our audio chunks
    const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
    
    try {
      // Create a form to send the audio file
      const formData = new FormData();
      formData.append('file', audioBlob, 'recording.webm');
      
      // Send the audio to your Python backend for processing
      const response = await axios.post('http://localhost:8000/api/transcribe', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      const transcribedText = response.data.text;
      
      // Add user message
      addMessage('user', transcribedText);
      
      // Get system response
      await getSystemResponse(transcribedText);
    } catch (error) {
      console.error('Error processing audio:', error);
      alert('Error processing audio. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  // Handle text input submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!inputText.trim()) return;
    
    const userMessage = inputText;
    setInputText('');
    
    // Add user message to chat
    addMessage('user', userMessage);
    
    // Process the message and get a response
    await getSystemResponse(userMessage);
  };

  // Add a message to the chat
  const addMessage = (role, content) => {
    setMessages(prev => [...prev, { role, content }]);
  };

  // Get response from the system
  const getSystemResponse = async (userInput) => {
    setIsProcessing(true);
    
    try {
      // Call your Python backend API
      const response = await axios.post('http://localhost:8000/api/chat', {
        message: userInput
      });
      
      // Add system message
      addMessage('system', response.data.text);
    } catch (error) {
      console.error('Error getting response:', error);
      addMessage('system', 'Sorry, I encountered an error processing your request.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto">
      {/* Chat messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div 
            key={index} 
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div 
              className={`max-w-xs sm:max-w-md md:max-w-lg rounded-lg p-3 ${
                message.role === 'user' 
                  ? 'bg-blue-500 text-white rounded-br-none' 
                  : 'bg-gray-200 text-gray-800 rounded-bl-none'
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input area */}
      <div className="border-t p-4 bg-white">
        {isProcessing && (
          <div className="text-sm text-gray-500 mb-2">Processing...</div>
        )}
        
        <form onSubmit={handleSubmit} className="flex items-center gap-2">
          <button
            type="button"
            onClick={isRecording ? stopRecording : startRecording}
            disabled={isProcessing}
            className={`p-2 rounded-full ${
              isRecording 
                ? 'bg-red-500 text-white' 
                : 'bg-gray-200 hover:bg-gray-300'
            }`}
            aria-label={isRecording ? 'Stop recording' : 'Start recording'}
          >
            {isRecording ? <MicOff size={20} /> : <Mic size={20} />}
          </button>
          
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            disabled={isProcessing || isRecording}
            placeholder={isRecording ? 'Recording...' : 'Type a message...'}
            className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          
          <button
            type="submit"
            disabled={!inputText.trim() || isProcessing || isRecording}
            className={`p-2 rounded-full ${
              !inputText.trim() || isProcessing || isRecording
                ? 'bg-gray-200 text-gray-400'
                : 'bg-blue-500 text-white hover:bg-blue-600'
            }`}
            aria-label="Send message"
          >
            <Send size={20} />
          </button>
        </form>
      </div>
    </div>
  );
}