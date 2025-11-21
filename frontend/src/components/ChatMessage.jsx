import React from 'react';
import { motion } from 'framer-motion';
import { User, Bot, Clock } from 'lucide-react';

const ChatMessage = ({ message, isTyping = false }) => {
  const isUser = message?.role === 'user';
  const isAssistant = message?.role === 'assistant';

  if (isTyping) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-start gap-3 mb-4"
      >
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-muted flex items-center justify-center">
          <Bot className="w-4 h-4 text-muted-foreground" />
        </div>
        <div className="typing-indicator glass-effect rounded-2xl">
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
          <div className="typing-dot"></div>
        </div>
      </motion.div>
    );
  }

  if (!message) return null;

  const messageText = message.parts?.map(part => 
    part.type === 'text' ? part.text : ''
  ).join('') || message.content || '';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className={`flex items-start gap-3 mb-4 ${isUser ? 'flex-row-reverse' : ''}`}
    >
      {/* Avatar */}
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        isUser ? 'bg-primary text-primary-foreground' : 'bg-muted'
      }`}>
        {isUser ? (
          <User className="w-4 h-4" />
        ) : (
          <Bot className="w-4 h-4 text-muted-foreground" />
        )}
      </div>

      {/* Message Content */}
      <div className={`flex flex-col max-w-[80%] ${isUser ? 'items-end' : 'items-start'}`}>
        <div className={`message-bubble ${isUser ? 'user' : 'assistant'} hover-lift`}>
          <p className="text-sm leading-relaxed whitespace-pre-wrap">
            {messageText}
          </p>
        </div>
        
        {/* Timestamp */}
        <div className="flex items-center gap-1 mt-1 px-2">
          <Clock className="w-3 h-3 text-muted-foreground" />
          <span className="text-xs text-muted-foreground">
            {message.createdAt ? 
              new Date(message.createdAt).toLocaleTimeString('ar-SA', {
                hour: '2-digit',
                minute: '2-digit'
              }) : 
              new Date().toLocaleTimeString('ar-SA', {
                hour: '2-digit',
                minute: '2-digit'
              })
            }
          </span>
        </div>
      </div>
    </motion.div>
  );
};

export default ChatMessage;

