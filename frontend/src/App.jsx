import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import ChatHeader from './components/ChatHeader';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import Sidebar from './components/Sidebar';
import { ScrollArea } from './components/ui/scroll-area';
import './App.css';

// Mock data for demonstration
const mockConversations = [
  {
    id: '1',
    title: 'مساعدة في البرمجة',
    lastMessage: 'كيف يمكنني تعلم React؟',
    updatedAt: new Date().toISOString(),
  },
  {
    id: '2',
    title: 'أسئلة عامة',
    lastMessage: 'ما هو الذكاء الاصطناعي؟',
    updatedAt: new Date(Date.now() - 86400000).toISOString(),
  },
];

function App() {
  const [messages, setMessages] = useState([
    {
      id: '1',
      role: 'assistant',
      parts: [{ type: 'text', text: 'مرحباً! أنا TR5، روبوت الدردشة الذكي. كيف يمكنني مساعدتك اليوم؟' }],
      createdAt: new Date().toISOString(),
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [currentChatId, setCurrentChatId] = useState('1');
  const [isConnected, setIsConnected] = useState(true);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSendMessage = async (text) => {
    if (!text.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      parts: [{ type: 'text', text }],
      createdAt: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setIsTyping(true);

    // Simulate API call delay
    setTimeout(() => {
      setIsTyping(false);
      
      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        parts: [{ 
          type: 'text', 
          text: `شكراً لك على رسالتك: "${text}". هذه استجابة تجريبية من TR5. في التطبيق الحقيقي، سيتم إرسال هذه الرسالة إلى Deep Seek أو Hugging Face للحصول على استجابة ذكية.` 
        }],
        createdAt: new Date().toISOString(),
      };

      setMessages(prev => [...prev, assistantMessage]);
      setIsLoading(false);
    }, 2000);
  };

  const handleStop = () => {
    setIsLoading(false);
    setIsTyping(false);
  };

  const handleNewChat = () => {
    setMessages([
      {
        id: Date.now().toString(),
        role: 'assistant',
        parts: [{ type: 'text', text: 'مرحباً! أنا TR5، روبوت الدردشة الذكي. كيف يمكنني مساعدتك اليوم؟' }],
        createdAt: new Date().toISOString(),
      }
    ]);
    setCurrentChatId(Date.now().toString());
    setIsSidebarOpen(false);
  };

  const handleSelectChat = (chatId) => {
    setCurrentChatId(chatId);
    setIsSidebarOpen(false);
    // In a real app, you would load the chat messages here
  };

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleOpenSettings = () => {
    // Handle settings modal
    console.log('Open settings');
  };

  return (
    <div className="dark min-h-screen bg-background text-foreground flex">
      {/* Sidebar */}
      <Sidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        conversations={mockConversations}
        onNewChat={handleNewChat}
        onSelectChat={handleSelectChat}
        currentChatId={currentChatId}
      />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-h-screen">
        {/* Header */}
        <ChatHeader
          onToggleSidebar={toggleSidebar}
          isConnected={isConnected}
          onOpenSettings={handleOpenSettings}
        />

        {/* Messages Area */}
        <div className="flex-1 relative">
          <ScrollArea className="h-full">
            <div className="max-w-4xl mx-auto px-4 py-6 space-y-4">
              {/* Welcome Message */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center py-8"
              >
                <motion.div
                  animate={{ 
                    rotate: [0, 360],
                    scale: [1, 1.1, 1]
                  }}
                  transition={{ 
                    rotate: { duration: 20, repeat: Infinity, ease: "linear" },
                    scale: { duration: 2, repeat: Infinity }
                  }}
                  className="w-16 h-16 bg-gradient-to-br from-accent to-primary rounded-2xl flex items-center justify-center mx-auto mb-4"
                >
                  <span className="text-2xl font-bold text-accent-foreground">TR5</span>
                </motion.div>
                <h2 className="text-2xl font-bold mb-2">مرحباً بك في TR5</h2>
                <p className="text-muted-foreground">روبوت الدردشة الذكي المدعوم بـ Deep Seek و Hugging Face</p>
              </motion.div>

              {/* Messages */}
              {messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))}

              {/* Typing Indicator */}
              {isTyping && <ChatMessage isTyping={true} />}

              {/* Scroll Anchor */}
              <div ref={messagesEndRef} />
            </div>
          </ScrollArea>

          {/* Scroll to Bottom Button */}
          {messages.length > 3 && (
            <motion.button
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={scrollToBottom}
              className="absolute bottom-20 right-4 w-10 h-10 bg-primary text-primary-foreground rounded-full flex items-center justify-center shadow-lg hover-glow"
            >
              ↓
            </motion.button>
          )}
        </div>

        {/* Input Area */}
        <ChatInput
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
          onStop={handleStop}
        />
      </div>
    </div>
  );
}

export default App;
