import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  MessageSquare, 
  Plus, 
  History, 
  Settings, 
  User, 
  Trash2, 
  Edit3,
  X
} from 'lucide-react';
import { Button } from './ui/button';
import { ScrollArea } from './ui/scroll-area';

const Sidebar = ({ isOpen, onClose, conversations = [], onNewChat, onSelectChat, currentChatId }) => {
  const sidebarVariants = {
    open: {
      x: 0,
      transition: {
        type: "spring",
        stiffness: 300,
        damping: 30
      }
    },
    closed: {
      x: "-100%",
      transition: {
        type: "spring",
        stiffness: 300,
        damping: 30
      }
    }
  };

  const overlayVariants = {
    open: { opacity: 1 },
    closed: { opacity: 0 }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Overlay */}
          <motion.div
            initial="closed"
            animate="open"
            exit="closed"
            variants={overlayVariants}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
            onClick={onClose}
          />

          {/* Sidebar */}
          <motion.aside
            initial="closed"
            animate="open"
            exit="closed"
            variants={sidebarVariants}
            className="fixed left-0 top-0 h-full w-80 bg-sidebar border-r border-sidebar-border z-50 lg:relative lg:z-auto"
          >
            <div className="flex flex-col h-full">
              {/* Header */}
              <div className="flex items-center justify-between p-4 border-b border-sidebar-border">
                <h2 className="text-lg font-semibold text-sidebar-foreground">المحادثات</h2>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={onClose}
                  className="lg:hidden hover-glow"
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>

              {/* New Chat Button */}
              <div className="p-4">
                <Button
                  onClick={onNewChat}
                  className="w-full justify-start gap-2 hover-glow ripple-effect"
                  variant="default"
                >
                  <Plus className="w-4 h-4" />
                  محادثة جديدة
                </Button>
              </div>

              {/* Conversations List */}
              <ScrollArea className="flex-1 px-2">
                <div className="space-y-2 pb-4">
                  {conversations.length === 0 ? (
                    <div className="text-center py-8 text-muted-foreground">
                      <MessageSquare className="w-8 h-8 mx-auto mb-2 opacity-50" />
                      <p className="text-sm">لا توجد محادثات بعد</p>
                    </div>
                  ) : (
                    conversations.map((chat) => (
                      <motion.div
                        key={chat.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className={`group relative rounded-lg p-3 cursor-pointer transition-all hover:bg-sidebar-accent ${
                          currentChatId === chat.id ? 'bg-sidebar-accent' : ''
                        }`}
                        onClick={() => onSelectChat(chat.id)}
                      >
                        <div className="flex items-start gap-3">
                          <MessageSquare className="w-4 h-4 text-sidebar-foreground mt-0.5 flex-shrink-0" />
                          <div className="flex-1 min-w-0">
                            <h3 className="text-sm font-medium text-sidebar-foreground truncate">
                              {chat.title || 'محادثة جديدة'}
                            </h3>
                            <p className="text-xs text-muted-foreground truncate mt-1">
                              {chat.lastMessage || 'ابدأ محادثة...'}
                            </p>
                            <div className="flex items-center gap-2 mt-2">
                              <History className="w-3 h-3 text-muted-foreground" />
                              <span className="text-xs text-muted-foreground">
                                {chat.updatedAt ? 
                                  new Date(chat.updatedAt).toLocaleDateString('ar-SA') : 
                                  'اليوم'
                                }
                              </span>
                            </div>
                          </div>
                        </div>

                        {/* Action Buttons */}
                        <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity flex gap-1">
                          <Button
                            variant="ghost"
                            size="icon"
                            className="w-6 h-6 hover:bg-sidebar-accent"
                            onClick={(e) => {
                              e.stopPropagation();
                              // Handle edit
                            }}
                          >
                            <Edit3 className="w-3 h-3" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="icon"
                            className="w-6 h-6 hover:bg-destructive hover:text-destructive-foreground"
                            onClick={(e) => {
                              e.stopPropagation();
                              // Handle delete
                            }}
                          >
                            <Trash2 className="w-3 h-3" />
                          </Button>
                        </div>
                      </motion.div>
                    ))
                  )}
                </div>
              </ScrollArea>

              {/* Footer */}
              <div className="border-t border-sidebar-border p-4 space-y-2">
                <Button
                  variant="ghost"
                  className="w-full justify-start gap-2 hover-glow"
                >
                  <Settings className="w-4 h-4" />
                  الإعدادات
                </Button>
                <Button
                  variant="ghost"
                  className="w-full justify-start gap-2 hover-glow"
                >
                  <User className="w-4 h-4" />
                  الملف الشخصي
                </Button>
              </div>
            </div>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
};

export default Sidebar;

