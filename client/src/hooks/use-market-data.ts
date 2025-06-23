import { useQuery } from '@tanstack/react-query';

export function useMarketOverview() {
  return useQuery({
    queryKey: ['/api/market/overview'],
    refetchInterval: 30000, // Refetch every 30 seconds
  });
}

export function useNiftyData() {
  return useQuery({
    queryKey: ['/api/market/nifty'],
    refetchInterval: 5000, // Refetch every 5 seconds
  });
}

export function useOptionsChain() {
  return useQuery({
    queryKey: ['/api/market/options-chain'],
    refetchInterval: 10000, // Refetch every 10 seconds
  });
}

export function useTradingSignals() {
  return useQuery({
    queryKey: ['/api/signals'],
    refetchInterval: 15000, // Refetch every 15 seconds
  });
}

export function useWhatsappUsers() {
  return useQuery({
    queryKey: ['/api/whatsapp/users'],
  });
}

export function usePortfolioSummary() {
  return useQuery({
    queryKey: ['/api/portfolio/summary'],
    refetchInterval: 30000,
  });
}
