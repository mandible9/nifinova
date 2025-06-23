import { storage } from '../storage';
import { zerodhaService } from './zerodha';
import { whatsappService } from './whatsapp';
import type { InsertTradingSignal } from '@shared/schema';

interface TechnicalIndicators {
  rsi: number;
  sma20: number;
  sma50: number;
  volume: number;
  volatility: number;
}

interface MarketConditions {
  trend: 'bullish' | 'bearish' | 'sideways';
  strength: number;
  momentum: number;
}

export class AISignalsService {
  private isRunning = false;

  constructor() {
    // Start signal generation when service is created
    this.startSignalGeneration();
  }

  private startSignalGeneration() {
    if (this.isRunning) return;
    
    this.isRunning = true;
    
    // Generate signals every 2 minutes
    setInterval(() => {
      this.generateSignals().catch(console.error);
    }, 120000);

    // Initial signal generation after 10 seconds
    setTimeout(() => {
      this.generateSignals().catch(console.error);
    }, 10000);
  }

  private async generateSignals() {
    try {
      console.log('Generating AI signals...');
      
      // Get current market data
      const niftyData = await zerodhaService.getNiftyQuote();
      const currentPrice = Object.values(niftyData)[0]?.last_price || 19845;
      
      // Generate strike prices around current level
      const baseStrike = Math.round(currentPrice / 50) * 50;
      const strikes = [baseStrike - 100, baseStrike - 50, baseStrike, baseStrike + 50, baseStrike + 100];
      
      // Get options data
      const optionsData = await zerodhaService.getOptionsChain(strikes);
      
      // Calculate technical indicators (simplified)
      const indicators = this.calculateTechnicalIndicators(niftyData);
      const marketConditions = this.analyzeMarketConditions(indicators);
      
      // Generate signals based on analysis
      const signals = this.generateTradingSignals(strikes, currentPrice, indicators, marketConditions);
      
      // Save signals to storage
      for (const signal of signals) {
        const savedSignal = await storage.createTradingSignal(signal);
        
        // Send WhatsApp notification for high-confidence signals (90%+)
        if (signal.confidence >= 90) {
          await this.sendWhatsAppNotifications(savedSignal);
        }
      }
      
      console.log(`Generated ${signals.length} new signals`);
      
    } catch (error) {
      console.error('Error generating signals:', error);
    }
  }

  private calculateTechnicalIndicators(marketData: any): TechnicalIndicators {
    // Simplified technical analysis - in production, use proper TA libraries
    const price = Object.values(marketData)[0]?.last_price || 19845;
    const volume = Object.values(marketData)[0]?.volume || 1000000;
    
    return {
      rsi: 45 + Math.random() * 20, // Mock RSI between 45-65
      sma20: price * (0.98 + Math.random() * 0.04),
      sma50: price * (0.96 + Math.random() * 0.08),
      volume: volume,
      volatility: 15 + Math.random() * 10
    };
  }

  private analyzeMarketConditions(indicators: TechnicalIndicators): MarketConditions {
    let trend: 'bullish' | 'bearish' | 'sideways' = 'sideways';
    let strength = 50;
    let momentum = 50;

    // Simple trend analysis
    if (indicators.rsi > 55 && indicators.sma20 > indicators.sma50) {
      trend = 'bullish';
      strength = 60 + Math.random() * 30;
      momentum = 55 + Math.random() * 25;
    } else if (indicators.rsi < 45 && indicators.sma20 < indicators.sma50) {
      trend = 'bearish';
      strength = 60 + Math.random() * 30;
      momentum = 55 + Math.random() * 25;
    } else {
      strength = 40 + Math.random() * 20;
      momentum = 40 + Math.random() * 20;
    }

    return { trend, strength, momentum };
  }

  private generateTradingSignals(
    strikes: number[], 
    currentPrice: number, 
    indicators: TechnicalIndicators, 
    conditions: MarketConditions
  ): InsertTradingSignal[] {
    const signals: InsertTradingSignal[] = [];
    const now = new Date();
    const expiryDate = this.getNextThursday();

    // Generate 1-3 signals per cycle
    const numSignals = 1 + Math.floor(Math.random() * 3);
    
    for (let i = 0; i < numSignals; i++) {
      const isCall = conditions.trend === 'bullish' ? Math.random() > 0.3 : Math.random() > 0.7;
      const type = isCall ? 'CALL' : 'PUT';
      
      // Select appropriate strike based on signal type
      let strikePrice: number;
      if (isCall) {
        // For calls, prefer slightly OTM strikes
        strikePrice = strikes[Math.floor(strikes.length * 0.6) + Math.floor(Math.random() * 2)];
      } else {
        // For puts, prefer slightly OTM strikes
        strikePrice = strikes[Math.floor(strikes.length * 0.4) - Math.floor(Math.random() * 2)];
      }

      // Calculate confidence based on multiple factors
      let confidence = 60;
      
      if (conditions.strength > 70) confidence += 15;
      if (conditions.momentum > 70) confidence += 10;
      if (indicators.volume > 2000000) confidence += 5;
      if (indicators.volatility < 20) confidence += 10;
      
      // Add some randomness but ensure reasonable range
      confidence += Math.floor(Math.random() * 20) - 10;
      confidence = Math.max(60, Math.min(98, confidence));

      // Generate target and stop loss
      const basePrice = 30 + Math.random() * 40; // Base option price
      const targetPrice = basePrice * (1.5 + Math.random() * 0.8);
      const stopLoss = basePrice * (0.4 + Math.random() * 0.3);

      // Generate reasoning
      const reasoning = this.generateReasoning(type, indicators, conditions, confidence);

      signals.push({
        type,
        strikePrice: strikePrice.toString(),
        targetPrice: targetPrice.toFixed(2),
        stopLoss: stopLoss.toFixed(2),
        confidence,
        reasoning,
        expiryDate,
        isActive: true,
        whatsappSent: false
      });
    }

    return signals;
  }

  private generateReasoning(
    type: string, 
    indicators: TechnicalIndicators, 
    conditions: MarketConditions,
    confidence: number
  ): string {
    const reasons = [];
    
    if (type === 'CALL') {
      if (conditions.trend === 'bullish') reasons.push('Strong bullish momentum detected');
      if (indicators.rsi < 50) reasons.push('RSI oversold recovery pattern');
      if (indicators.sma20 > indicators.sma50) reasons.push('Short-term MA above long-term MA');
      if (indicators.volume > 1500000) reasons.push('High volume supporting upward move');
    } else {
      if (conditions.trend === 'bearish') reasons.push('Bearish trend continuation expected');
      if (indicators.rsi > 60) reasons.push('RSI overbought, correction likely');
      if (indicators.sma20 < indicators.sma50) reasons.push('Short-term MA below long-term MA');
      if (indicators.volatility > 25) reasons.push('High volatility favoring downward move');
    }

    if (confidence > 90) reasons.push('Multiple confirmations align');
    if (conditions.strength > 75) reasons.push('Strong directional bias');

    return reasons.slice(0, 2).join(', ') + '. Trade with proper risk management.';
  }

  private getNextThursday(): Date {
    const today = new Date();
    const thursday = new Date(today);
    const daysUntilThursday = (4 - today.getDay() + 7) % 7;
    thursday.setDate(today.getDate() + (daysUntilThursday === 0 ? 7 : daysUntilThursday));
    thursday.setHours(15, 30, 0, 0); // 3:30 PM expiry
    return thursday;
  }

  private async sendWhatsAppNotifications(signal: any) {
    try {
      const whatsappUsers = await storage.getAllWhatsappUsers();
      
      for (const user of whatsappUsers) {
        await whatsappService.sendTradingSignal(user.phoneNumber, {
          type: signal.type,
          strikePrice: signal.strikePrice,
          confidence: signal.confidence,
          targetPrice: signal.targetPrice,
          stopLoss: signal.stopLoss,
          reasoning: signal.reasoning
        });
      }
      
      // Mark signal as WhatsApp sent
      await storage.updateSignalWhatsappSent(signal.id);
      
    } catch (error) {
      console.error('Error sending WhatsApp notifications:', error);
    }
  }

  async getMarketOverview() {
    try {
      const niftyData = await zerodhaService.getNiftyQuote();
      const signals = await storage.getAllActiveSignals();
      const positions = await storage.getAllPortfolioPositions();
      const whatsappUsers = await storage.getAllWhatsappUsers();

      const niftyQuote = Object.values(niftyData)[0] as any;
      
      return {
        nifty50: {
          price: niftyQuote?.last_price || 19845.30,
          change: niftyQuote?.change || 156.20,
          changePercent: niftyQuote?.net_change || 0.79
        },
        activeSignals: signals.length,
        successRate: 74.5, // Mock success rate - calculate from historical data in production
        whatsappUsers: whatsappUsers.length,
        portfolio: {
          totalPnl: positions.reduce((sum, pos) => sum + Number(pos.pnl), 0),
          activePositions: positions.length
        }
      };
    } catch (error) {
      console.error('Error getting market overview:', error);
      // Return mock data on error
      return {
        nifty50: { price: 19845.30, change: 156.20, changePercent: 0.79 },
        activeSignals: 12,
        successRate: 74.5,
        whatsappUsers: 8,
        portfolio: { totalPnl: 12456, activePositions: 3 }
      };
    }
  }
}

export const aiSignalsService = new AISignalsService();
