import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { useTradingSignals } from '@/hooks/use-market-data';
import { MessageSquare } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

export function AISignals() {
  const { data: signals, isLoading } = useTradingSignals();

  if (isLoading) {
    return (
      <Card className="shadow-sm border border-gray-200">
        <CardHeader>
          <CardTitle className="text-lg font-semibold text-gray-900">Live AI Signals</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="p-4 rounded-lg border">
              <Skeleton className="h-6 w-32 mb-2" />
              <Skeleton className="h-4 w-full mb-2" />
              <Skeleton className="h-4 w-24" />
            </div>
          ))}
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="shadow-sm border border-gray-200">
      <CardHeader className="border-b border-gray-200">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold text-gray-900">Live AI Signals</CardTitle>
          <Badge variant="secondary" className="bg-green-100 text-green-800">
            Real-time
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="p-6 space-y-4">
        {signals?.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <p>No active signals at the moment</p>
            <p className="text-sm">New AI signals will appear here</p>
          </div>
        ) : (
          signals?.slice(0, 3).map((signal: any) => (
            <div
              key={signal.id}
              className={`border-l-4 p-4 rounded-r-lg relative ${
                signal.type === 'CALL'
                  ? 'border-green-500 bg-green-50'
                  : 'border-red-500 bg-red-50'
              }`}
            >
              {signal.whatsappSent && (
                <div className="absolute top-2 right-2">
                  <MessageSquare className="text-green-600" size={16} title="WhatsApp Alert Sent" />
                </div>
              )}
              
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-2">
                  <Badge
                    className={`text-white text-xs font-bold ${
                      signal.type === 'CALL' ? 'bg-green-600' : 'bg-red-600'
                    }`}
                  >
                    {signal.type}
                  </Badge>
                  <span className="font-medium">{signal.strikePrice} {signal.type === 'CALL' ? 'CE' : 'PE'}</span>
                </div>
                <span
                  className={`font-bold text-sm ${
                    signal.confidence >= 90
                      ? 'text-green-600'
                      : signal.confidence >= 75
                      ? 'text-orange-600'
                      : 'text-gray-600'
                  }`}
                >
                  {signal.confidence}% Confidence
                </span>
              </div>
              
              <p className="text-sm text-gray-600 mb-2">{signal.reasoning}</p>
              
              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>Target: ₹{signal.targetPrice} | SL: ₹{signal.stopLoss}</span>
                <span>
                  {signal.createdAt 
                    ? formatDistanceToNow(new Date(signal.createdAt), { addSuffix: true })
                    : 'Just now'
                  }
                </span>
              </div>
            </div>
          ))
        )}
      </CardContent>
    </Card>
  );
}
