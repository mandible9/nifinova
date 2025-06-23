interface ZerodhaQuote {
  instrument_token: number;
  last_price: number;
  change: number;
  net_change: number;
  volume: number;
}

interface ZerodhaOptionsData {
  [key: string]: {
    call?: ZerodhaQuote;
    put?: ZerodhaQuote;
  };
}

export class ZerodhaService {
  private apiKey: string;
  private accessToken: string;
  private baseUrl = 'https://api.kite.trade';

  constructor() {
    this.apiKey = process.env.ZERODHA_API_KEY || process.env.KITE_API_KEY || '';
    this.accessToken = process.env.ZERODHA_ACCESS_TOKEN || process.env.KITE_ACCESS_TOKEN || '';
  }

  private async makeRequest(endpoint: string): Promise<any> {
    if (!this.apiKey || !this.accessToken) {
      // Return mock data for demo purposes when API keys are not available
      return this.getMockData(endpoint);
    }
    
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        headers: {
          'Authorization': `token ${this.apiKey}:${this.accessToken}`,
          'X-Kite-Version': '3'
        }
      });

      if (!response.ok) {
        throw new Error(`Zerodha API error: ${response.status}`);
      }

      const data = await response.json();
      return data.data;
    } catch (error) {
      console.error('Zerodha API error:', error);
      // Fallback to mock data on error
      return this.getMockData(endpoint);
    }
  }

  private getMockData(endpoint: string): any {
    if (endpoint.includes('quote')) {
      return {
        '256265': {
          instrument_token: 256265,
          last_price: 19845.30,
          change: 156.20,
          net_change: 0.79,
          volume: 1234567
        }
      };
    } else if (endpoint.includes('instruments')) {
      // Mock options chain data
      return this.generateMockOptionsChain();
    }
    return {};
  }

  private generateMockOptionsChain() {
    const strikes = [19750, 19800, 19850, 19900, 19950];
    const data: any = {};
    
    strikes.forEach((strike, index) => {
      data[`${strike}CE`] = {
        instrument_token: 20000000 + strike,
        last_price: Math.max(5, 100 - (index * 25) + Math.random() * 20),
        change: (Math.random() - 0.5) * 10,
        net_change: (Math.random() - 0.5) * 5,
        volume: Math.floor(Math.random() * 500000) + 50000
      };
      
      data[`${strike}PE`] = {
        instrument_token: 30000000 + strike,
        last_price: Math.max(5, 20 + (index * 15) + Math.random() * 20),
        change: (Math.random() - 0.5) * 10,
        net_change: (Math.random() - 0.5) * 5,
        volume: Math.floor(Math.random() * 400000) + 40000
      };
    });
    
    return data;
  }

  async getNiftyQuote() {
    const data = await this.makeRequest('/quote?i=NSE:NIFTY 50');
    return data;
  }

  async getOptionsChain(strikes: number[]) {
    const instruments = strikes.flatMap(strike => [
      `NFO:NIFTY${new Date().getFullYear().toString().slice(-2)}${this.getExpiryString()}${strike}CE`,
      `NFO:NIFTY${new Date().getFullYear().toString().slice(-2)}${this.getExpiryString()}${strike}PE`
    ]);
    
    const instrumentsQuery = instruments.join('&i=');
    const data = await this.makeRequest(`/quote?i=${instrumentsQuery}`);
    return data;
  }

  private getExpiryString(): string {
    // Get current week's Thursday (typical Nifty expiry)
    const today = new Date();
    const thursday = new Date(today);
    thursday.setDate(today.getDate() + (4 - today.getDay()));
    
    const month = (thursday.getMonth() + 1).toString().padStart(2, '0');
    const date = thursday.getDate().toString().padStart(2, '0');
    
    return `${month}${date}`;
  }

  async getHistoricalData(instrument: string, from: Date, to: Date, interval: string = 'minute') {
    const fromStr = from.toISOString().split('T')[0];
    const toStr = to.toISOString().split('T')[0];
    
    const data = await this.makeRequest(
      `/instruments/historical/${instrument}/${interval}?from=${fromStr}&to=${toStr}`
    );
    return data;
  }
}

export const zerodhaService = new ZerodhaService();
