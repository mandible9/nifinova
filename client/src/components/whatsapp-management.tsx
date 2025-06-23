import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Skeleton } from '@/components/ui/skeleton';
import { useWhatsappUsers } from '@/hooks/use-market-data';
import { useToast } from '@/hooks/use-toast';
import { apiRequest } from '@/lib/queryClient';
import { queryClient } from '@/lib/queryClient';
import { MessageSquare, Trash2, Plus } from 'lucide-react';

export function WhatsAppManagement() {
  const { data: users, isLoading } = useWhatsappUsers();
  const [newNumber, setNewNumber] = useState('');
  const [isAdding, setIsAdding] = useState(false);
  const { toast } = useToast();

  const handleAddUser = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newNumber.trim()) return;

    setIsAdding(true);
    try {
      await apiRequest('POST', '/api/whatsapp/users', { phoneNumber: newNumber });
      
      toast({
        title: "User Added",
        description: "WhatsApp user added successfully. Welcome message sent!",
      });
      
      setNewNumber('');
      queryClient.invalidateQueries({ queryKey: ['/api/whatsapp/users'] });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Failed to Add User",
        description: error instanceof Error ? error.message : "Please check the phone number format",
      });
    } finally {
      setIsAdding(false);
    }
  };

  const handleRemoveUser = async (phoneNumber: string) => {
    try {
      await apiRequest('DELETE', `/api/whatsapp/users/${encodeURIComponent(phoneNumber)}`);
      
      toast({
        title: "User Removed",
        description: "WhatsApp user removed successfully",
      });
      
      queryClient.invalidateQueries({ queryKey: ['/api/whatsapp/users'] });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Failed to Remove User",
        description: "Please try again",
      });
    }
  };

  if (isLoading) {
    return (
      <Card className="shadow-sm border border-gray-200">
        <CardHeader>
          <CardTitle>WhatsApp Notifications</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {Array.from({ length: 3 }).map((_, i) => (
            <Skeleton key={i} className="h-12 w-full" />
          ))}
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="shadow-sm border border-gray-200">
      <CardHeader className="border-b border-gray-200">
        <CardTitle className="text-lg font-semibold text-gray-900">WhatsApp Notifications</CardTitle>
        <p className="text-sm text-gray-500">Manage users receiving strong buy signals</p>
      </CardHeader>
      <CardContent className="p-6">
        <div className="space-y-4 mb-6">
          {users?.length === 0 ? (
            <div className="text-center py-4 text-gray-500">
              <MessageSquare className="mx-auto mb-2" size={24} />
              <p>No WhatsApp users added yet</p>
              <p className="text-sm">Add numbers to receive trading alerts</p>
            </div>
          ) : (
            users?.map((user: any) => (
              <div key={user.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <MessageSquare className="text-green-600" size={16} />
                  <span className="font-medium">{user.phoneNumber}</span>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleRemoveUser(user.phoneNumber)}
                  className="text-red-600 hover:text-red-700 hover:bg-red-50"
                >
                  <Trash2 size={16} />
                </Button>
              </div>
            ))
          )}
        </div>
        
        <div className="border-t border-gray-200 pt-4">
          <h4 className="font-medium text-gray-900 mb-3">Add New Number</h4>
          <form onSubmit={handleAddUser} className="flex space-x-2">
            <Input
              type="tel"
              value={newNumber}
              onChange={(e) => setNewNumber(e.target.value)}
              placeholder="+91 XXXXX XXXXX"
              className="flex-1"
              disabled={isAdding}
            />
            <Button 
              type="submit" 
              disabled={isAdding || !newNumber.trim()}
              className="bg-blue-600 hover:bg-blue-700 text-white"
            >
              {isAdding ? (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              ) : (
                <Plus size={16} />
              )}
            </Button>
          </form>
        </div>
      </CardContent>
    </Card>
  );
}
