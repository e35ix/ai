import React from 'react';
import { motion } from 'framer-motion';
import { Settings, Menu, Zap, Wifi, WifiOff } from 'lucide-react';
import { Button } from './ui/button';

const ChatHeader = ({ onToggleSidebar, isConnected = true, onOpenSettings }) => {
  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="sticky top-0 z-50 glass-effect border-b border-border"
    >
      <div className="flex items-center justify-between px-4 py-3">
        {/* Left Section */}
        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            size="icon"
            onClick={onToggleSidebar}
            className="hover-glow"
          >
            <Menu className="w-5 h-5" />
          </Button>
          
          {/* Logo and Title */}
          <div className="flex items-center gap-3">
            <motion.div
              animate={{ rotate: [0, 360] }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              className="w-8 h-8 bg-gradient-to-br from-accent to-primary rounded-lg flex items-center justify-center"
            >
              <Zap className="w-4 h-4 text-accent-foreground" />
            </motion.div>
            <div>
              <h1 className="text-lg font-bold text-foreground">TR5</h1>
              <p className="text-xs text-muted-foreground">روبوت الدردشة الذكي</p>
            </div>
          </div>
        </div>

        {/* Center Section - Status */}
        <div className="hidden md:flex items-center gap-2">
          <motion.div
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
            className={`w-2 h-2 rounded-full ${
              isConnected ? 'bg-green-500' : 'bg-red-500'
            }`}
          />
          <span className="text-sm text-muted-foreground">
            {isConnected ? 'متصل' : 'غير متصل'}
          </span>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-2">
          {/* Connection Status (Mobile) */}
          <div className="md:hidden">
            {isConnected ? (
              <Wifi className="w-4 h-4 text-green-500" />
            ) : (
              <WifiOff className="w-4 h-4 text-red-500" />
            )}
          </div>

          {/* Settings Button */}
          <Button
            variant="ghost"
            size="icon"
            onClick={onOpenSettings}
            className="hover-glow"
          >
            <Settings className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Progress Bar (when loading) */}
      <motion.div
        initial={{ scaleX: 0 }}
        animate={{ scaleX: 1 }}
        className="h-0.5 bg-gradient-to-r from-accent via-primary to-accent origin-left"
        style={{ display: 'none' }} // Show when loading
      />
    </motion.header>
  );
};

export default ChatHeader;

