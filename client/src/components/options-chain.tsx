import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Skeleton } from '@/components/ui/skeleton';
import { useOptionsChain } from '@/hooks/use-market-data';

export function OptionsChain() {
  const { data: optionsData, isLoading } = useOptionsChain();

  // Transform the data into a more usable format
  const transformOptionsData = (data: any) => {
    if (!data) return [];
    
    const strikes = [19750, 19800, 19850, 19900, 19950];
    return strikes.map(strike => {
      const callKey = Object.keys(data).find(key => key.includes(`${strike}CE`));
      const putKey = Object.keys(data).find(key => key.includes(`${strike}PE`));
      
      const callData = callKey ? data[callKey] : null;
      const putData = putKey ? data[putKey] : null;
      
      return {
        strike,
        callLTP: callData?.last_price || 0,
        callVolume: callData?.volume || 0,
        putLTP: putData?.last_price || 0,
        putVolume: putData?.volume || 0,
        isATM: strike === 19850 // Mock ATM strike
      };
    });
  };

  const optionsChain = transformOptionsData(optionsData);

  if (isLoading) {
    return (
      <Card className="shadow-sm border border-gray-200">
        <CardHeader>
          <CardTitle>Nifty Options Chain</CardTitle>
        </CardHeader>
        <CardContent>
          <Skeleton className="h-64 w-full" />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="shadow-sm border border-gray-200">
      <CardHeader className="border-b border-gray-200">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold text-gray-900">Nifty Options Chain</CardTitle>
          <Select defaultValue="current">
            <SelectTrigger className="w-40">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="current">Current Week</SelectItem>
              <SelectItem value="next">Next Week</SelectItem>
              <SelectItem value="monthly">Monthly</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </CardHeader>
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left font-medium text-gray-700">Calls LTP</th>
                <th className="px-4 py-3 text-left font-medium text-gray-700">Calls Vol</th>
                <th className="px-4 py-3 text-center font-medium text-gray-700">Strike</th>
                <th className="px-4 py-3 text-right font-medium text-gray-700">Puts Vol</th>
                <th className="px-4 py-3 text-right font-medium text-gray-700">Puts LTP</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {optionsChain.map((option) => (
                <tr
                  key={option.strike}
                  className={`hover:bg-gray-50 ${
                    option.isATM ? 'bg-blue-50 border-2 border-blue-200' : ''
                  }`}
                >
                  <td className="px-4 py-3 text-green-600 font-medium">
                    {option.callLTP.toFixed(2)}
                  </td>
                  <td className="px-4 py-3 text-gray-600">
                    {option.callVolume.toLocaleString()}
                  </td>
                  <td className={`px-4 py-3 text-center font-bold ${
                    option.isATM 
                      ? 'text-blue-600 bg-yellow-50' 
                      : 'bg-yellow-50'
                  }`}>
                    {option.strike}
                  </td>
                  <td className="px-4 py-3 text-right text-gray-600">
                    {option.putVolume.toLocaleString()}
                  </td>
                  <td className="px-4 py-3 text-right text-red-600 font-medium">
                    {option.putLTP.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}
