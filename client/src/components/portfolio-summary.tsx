import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { usePortfolioSummary } from '@/hooks/use-market-data';

export function PortfolioSummary() {
  const { data: portfolio, isLoading } = usePortfolioSummary();

  if (isLoading) {
    return (
      <Card className="shadow-sm border border-gray-200">
        <CardHeader>
          <CardTitle>Portfolio Summary</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {Array.from({ length: 5 }).map((_, i) => (
            <Skeleton key={i} className="h-16 w-full" />
          ))}
        </CardContent>
      </Card>
    );
  }

  const totalPnl = Number(portfolio?.totalPnl || 0);
  const todayPnl = Number(portfolio?.todayPnl || 0);
  const totalPnlColor = totalPnl >= 0 ? 'text-green-600' : 'text-red-600';
  const todayPnlColor = todayPnl >= 0 ? 'text-green-600' : 'text-red-600';

  return (
    <Card className="shadow-sm border border-gray-200">
      <CardHeader className="border-b border-gray-200">
        <CardTitle className="text-lg font-semibold text-gray-900">Portfolio Summary</CardTitle>
      </CardHeader>
      <CardContent className="p-6 space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-gray-600">Total P&L</span>
          <span className={`font-bold ${totalPnlColor}`}>
            {totalPnl >= 0 ? '+' : ''}₹{Math.abs(totalPnl).toLocaleString()}
          </span>
        </div>
        
        <div className="flex items-center justify-between">
          <span className="text-gray-600">Today's P&L</span>
          <span className={`font-bold ${todayPnlColor}`}>
            {todayPnl >= 0 ? '+' : ''}₹{Math.abs(todayPnl).toLocaleString()}
          </span>
        </div>
        
        <div className="flex items-center justify-between">
          <span className="text-gray-600">Active Positions</span>
          <span className="font-medium">{portfolio?.activePositions || 0}</span>
        </div>
        
        {portfolio?.positions?.length > 0 && (
          <div className="border-t border-gray-200 pt-4 space-y-3">
            {portfolio.positions.slice(0, 3).map((position: any) => {
              const pnl = Number(position.pnl);
              const pnlColor = pnl >= 0 ? 'text-green-600' : 'text-red-600';
              const bgColor = pnl >= 0 ? 'bg-green-50' : 'bg-red-50';
              
              return (
                <div key={position.id} className={`${bgColor} p-3 rounded-lg`}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-medium text-sm">
                      {position.strikePrice} {position.type === 'CALL' ? 'CE' : 'PE'}
                    </span>
                    <span className={`${pnlColor} font-bold text-sm`}>
                      {pnl >= 0 ? '+' : ''}₹{Math.abs(pnl).toLocaleString()}
                    </span>
                  </div>
                  <div className="text-xs text-gray-600">
                    <span>Qty: {position.quantity}</span> | 
                    <span> LTP: ₹{Number(position.currentPrice).toFixed(2)}</span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
        
        {(!portfolio?.positions || portfolio.positions.length === 0) && (
          <div className="border-t border-gray-200 pt-4 text-center text-gray-500">
            <p>No active positions</p>
            <p className="text-sm">Start trading to see your portfolio</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
