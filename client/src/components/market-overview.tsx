import { Card, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { TrendingUp, ArrowUp, Bot, Target, MessageSquare } from 'lucide-react';

interface MarketOverviewProps {
  data: any;
  isLoading: boolean;
}

export function MarketOverview({ data, isLoading }: MarketOverviewProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {Array.from({ length: 4 }).map((_, i) => (
          <Card key={i} className="p-6">
            <Skeleton className="h-12 w-full mb-2" />
            <Skeleton className="h-8 w-24 mb-2" />
            <Skeleton className="h-6 w-32" />
          </Card>
        ))}
      </div>
    );
  }

  const nifty = data?.nifty50 || { price: 19845.30, change: 156.20, changePercent: 0.79 };
  const changeColor = nifty.change >= 0 ? 'text-green-600' : 'text-red-600';
  const ArrowIcon = nifty.change >= 0 ? ArrowUp : ArrowUp;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <Card className="shadow-sm border border-gray-200">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Nifty 50</p>
              <p className="text-2xl font-bold text-gray-900">
                {nifty.price.toLocaleString('en-IN', { maximumFractionDigits: 2 })}
              </p>
              <p className={`text-sm font-medium ${changeColor}`}>
                <ArrowIcon className="inline mr-1" size={12} />
                +{nifty.change.toFixed(2)} (+{nifty.changePercent.toFixed(2)}%)
              </p>
            </div>
            <div className="bg-blue-100 rounded-full p-3">
              <TrendingUp className="text-blue-600" size={20} />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="shadow-sm border border-gray-200">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Active Signals</p>
              <p className="text-2xl font-bold text-gray-900">{data?.activeSignals || 12}</p>
              <p className="text-orange-600 text-sm font-medium">
                <Bot className="inline mr-1" size={12} />
                AI Generated
              </p>
            </div>
            <div className="bg-orange-100 rounded-full p-3">
              <Bot className="text-orange-600" size={20} />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="shadow-sm border border-gray-200">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Success Rate</p>
              <p className="text-2xl font-bold text-gray-900">{data?.successRate || 74.5}%</p>
              <p className="text-green-600 text-sm font-medium">
                <ArrowUp className="inline mr-1" size={12} />
                +2.1% Today
              </p>
            </div>
            <div className="bg-green-100 rounded-full p-3">
              <Target className="text-green-600" size={20} />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="shadow-sm border border-gray-200">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">WhatsApp Users</p>
              <p className="text-2xl font-bold text-gray-900">{data?.whatsappUsers || 8}</p>
              <p className="text-gray-500 text-sm font-medium">
                <MessageSquare className="inline mr-1" size={12} />
                Notifications Active
              </p>
            </div>
            <div className="bg-green-100 rounded-full p-3">
              <MessageSquare className="text-green-600" size={20} />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
