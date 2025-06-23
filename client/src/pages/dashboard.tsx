import { Sidebar } from '@/components/sidebar';
import { MarketOverview } from '@/components/market-overview';
import { AISignals } from '@/components/ai-signals';
import { WhatsAppManagement } from '@/components/whatsapp-management';
import { OptionsChain } from '@/components/options-chain';
import { PortfolioSummary } from '@/components/portfolio-summary';
import { useMarketOverview } from '@/hooks/use-market-data';

export default function Dashboard() {
  const { data: marketData, isLoading } = useMarketOverview();

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      
      <div className="ml-64 min-h-screen">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Trading Dashboard</h1>
              <p className="text-gray-600">Nifty 50 Options Analysis</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                <div className="w-2 h-2 bg-green-500 rounded-full inline-block mr-1"></div>
                Connected to Zerodha
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-500">Last Update</p>
                <p className="font-medium">{new Date().toLocaleTimeString()}</p>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="p-6">
          {/* Market Overview Cards */}
          <MarketOverview data={marketData} isLoading={isLoading} />

          {/* AI Signals and WhatsApp Management */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <AISignals />
            <WhatsAppManagement />
          </div>

          {/* Options Chain and Portfolio */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <OptionsChain />
            </div>
            <PortfolioSummary />
          </div>
        </main>
      </div>
    </div>
  );
}
