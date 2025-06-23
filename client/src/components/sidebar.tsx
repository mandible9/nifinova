import { Button } from '@/components/ui/button';
import { useAuth } from '@/hooks/use-auth';
import { useToast } from '@/hooks/use-toast';
import { 
  TrendingUp, 
  BarChart3, 
  Bot, 
  MessageSquare, 
  Briefcase, 
  Settings, 
  LogOut,
  Home
} from 'lucide-react';

export function Sidebar() {
  const { logout } = useAuth();
  const { toast } = useToast();

  const handleLogout = async () => {
    try {
      await logout();
      toast({
        title: "Logged Out",
        description: "You have been successfully logged out",
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Logout Failed",
        description: "Failed to logout. Please try again.",
      });
    }
  };

  return (
    <div className="fixed inset-y-0 left-0 w-64 bg-white shadow-lg border-r border-gray-200 z-40">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="bg-blue-600 rounded-lg w-10 h-10 flex items-center justify-center">
            <TrendingUp className="text-white" size={20} />
          </div>
          <div>
            <h2 className="font-bold text-gray-900">Nifty AI</h2>
            <p className="text-sm text-gray-500">Trading Assistant</p>
          </div>
        </div>
      </div>
      
      <nav className="p-4 space-y-2">
        <Button
          variant="default"
          className="w-full justify-start bg-blue-600 text-white hover:bg-blue-700"
        >
          <Home className="mr-3" size={16} />
          Dashboard
        </Button>
        
        <Button variant="ghost" className="w-full justify-start text-gray-700 hover:bg-gray-100">
          <BarChart3 className="mr-3" size={16} />
          Options Chain
        </Button>
        
        <Button variant="ghost" className="w-full justify-start text-gray-700 hover:bg-gray-100">
          <Bot className="mr-3" size={16} />
          AI Signals
        </Button>
        
        <Button variant="ghost" className="w-full justify-start text-gray-700 hover:bg-gray-100">
          <MessageSquare className="mr-3" size={16} />
          WhatsApp Setup
        </Button>
        
        <Button variant="ghost" className="w-full justify-start text-gray-700 hover:bg-gray-100">
          <Briefcase className="mr-3" size={16} />
          Portfolio
        </Button>
        
        <Button variant="ghost" className="w-full justify-start text-gray-700 hover:bg-gray-100">
          <Settings className="mr-3" size={16} />
          Settings
        </Button>
      </nav>
      
      <div className="absolute bottom-4 left-4 right-4">
        <Button 
          variant="ghost" 
          onClick={handleLogout}
          className="w-full justify-start text-gray-700 hover:bg-gray-100"
        >
          <LogOut className="mr-3" size={16} />
          Logout
        </Button>
      </div>
    </div>
  );
}
