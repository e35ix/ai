import React, { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { Send, Paperclip, Mic, Square } from 'lucide-react';
import { Button } from './ui/button';

const ChatInput = ({ onSendMessage, isLoading = false, onStop }) => {
  const [input, setInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const textareaRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSendMessage(input.trim());
      setInput('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
    
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
    // Here you would implement voice recording functionality
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="sticky bottom-0 bg-background/80 backdrop-blur-lg border-t border-border p-4"
    >
      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
        <div className="relative flex items-end gap-2">
          {/* Attachment Button */}
          <Button
            type="button"
            variant="ghost"
            size="icon"
            className="flex-shrink-0 hover-glow"
            disabled={isLoading}
          >
            <Paperclip className="w-4 h-4" />
          </Button>

          {/* Input Field */}
          <div className="flex-1 relative">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              placeholder={isLoading ? "TR5 يكتب..." : "اكتب رسالتك هنا..."}
              disabled={isLoading}
              className="w-full min-h-[44px] max-h-[120px] px-4 py-3 pr-12 bg-input border border-border rounded-2xl resize-none input-focus text-sm leading-relaxed placeholder:text-muted-foreground disabled:opacity-50 disabled:cursor-not-allowed"
              rows={1}
            />
            
            {/* Character Counter */}
            {input.length > 0 && (
              <div className="absolute bottom-1 left-2 text-xs text-muted-foreground">
                {input.length}
              </div>
            )}
          </div>

          {/* Voice Recording Button */}
          <Button
            type="button"
            variant="ghost"
            size="icon"
            className={`flex-shrink-0 ${isRecording ? 'text-red-500 pulse-animation' : ''} hover-glow`}
            onClick={toggleRecording}
            disabled={isLoading}
          >
            <Mic className="w-4 h-4" />
          </Button>

          {/* Send/Stop Button */}
          {isLoading ? (
            <Button
              type="button"
              variant="destructive"
              size="icon"
              className="flex-shrink-0 ripple-effect"
              onClick={onStop}
            >
              <Square className="w-4 h-4" />
            </Button>
          ) : (
            <Button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="flex-shrink-0 ripple-effect hover-glow"
              size="icon"
            >
              <Send className="w-4 h-4" />
            </Button>
          )}
        </div>

        {/* Status Indicators */}
        <div className="flex items-center justify-between mt-2 px-2">
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            {isRecording && (
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ repeat: Infinity, duration: 1 }}
                className="w-2 h-2 bg-red-500 rounded-full"
              />
            )}
            {isRecording && "جاري التسجيل..."}
          </div>
          
          <div className="text-xs text-muted-foreground">
            {isLoading ? "TR5 يفكر..." : "اضغط Enter للإرسال"}
          </div>
        </div>
      </form>
    </motion.div>
  );
};

export default ChatInput;

