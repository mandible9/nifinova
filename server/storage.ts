import { 
  users, whatsappUsers, tradingSignals, portfolioPositions, marketData, optionsChain,
  type User, type InsertUser, type WhatsappUser, type InsertWhatsappUser,
  type TradingSignal, type InsertTradingSignal, type PortfolioPosition, type InsertPortfolioPosition,
  type MarketData, type InsertMarketData, type OptionsChain, type InsertOptionsChain
} from "@shared/schema";

export interface IStorage {
  // User operations
  getUser(id: number): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;

  // WhatsApp user operations
  getAllWhatsappUsers(): Promise<WhatsappUser[]>;
  addWhatsappUser(user: InsertWhatsappUser): Promise<WhatsappUser>;
  removeWhatsappUser(phoneNumber: string): Promise<boolean>;

  // Trading signal operations
  getAllActiveSignals(): Promise<TradingSignal[]>;
  createTradingSignal(signal: InsertTradingSignal): Promise<TradingSignal>;
  updateSignalWhatsappSent(id: number): Promise<boolean>;

  // Portfolio operations
  getAllPortfolioPositions(): Promise<PortfolioPosition[]>;
  createPortfolioPosition(position: InsertPortfolioPosition): Promise<PortfolioPosition>;
  updatePortfolioPosition(id: number, updates: Partial<PortfolioPosition>): Promise<PortfolioPosition | undefined>;

  // Market data operations
  getMarketData(symbol: string): Promise<MarketData | undefined>;
  updateMarketData(data: InsertMarketData): Promise<MarketData>;

  // Options chain operations
  getOptionsChain(expiryDate: Date): Promise<OptionsChain[]>;
  updateOptionsChain(data: InsertOptionsChain[]): Promise<OptionsChain[]>;
}

export class MemStorage implements IStorage {
  private users: Map<number, User>;
  private whatsappUsers: Map<number, WhatsappUser>;
  private tradingSignals: Map<number, TradingSignal>;
  private portfolioPositions: Map<number, PortfolioPosition>;
  private marketData: Map<string, MarketData>;
  private optionsChain: Map<string, OptionsChain>;
  
  private currentUserId: number;
  private currentWhatsappUserId: number;
  private currentSignalId: number;
  private currentPositionId: number;
  private currentMarketDataId: number;
  private currentOptionsChainId: number;

  constructor() {
    this.users = new Map();
    this.whatsappUsers = new Map();
    this.tradingSignals = new Map();
    this.portfolioPositions = new Map();
    this.marketData = new Map();
    this.optionsChain = new Map();
    
    this.currentUserId = 1;
    this.currentWhatsappUserId = 1;
    this.currentSignalId = 1;
    this.currentPositionId = 1;
    this.currentMarketDataId = 1;
    this.currentOptionsChainId = 1;

    // Initialize with admin user
    this.createUser({ username: "admin", password: "admin" });
  }

  // User operations
  async getUser(id: number): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(user => user.username === username);
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = this.currentUserId++;
    const user: User = { ...insertUser, id };
    this.users.set(id, user);
    return user;
  }

  // WhatsApp user operations
  async getAllWhatsappUsers(): Promise<WhatsappUser[]> {
    return Array.from(this.whatsappUsers.values()).filter(user => user.isActive);
  }

  async addWhatsappUser(insertUser: InsertWhatsappUser): Promise<WhatsappUser> {
    const id = this.currentWhatsappUserId++;
    const user: WhatsappUser = {
      ...insertUser,
      id,
      isActive: true,
      createdAt: new Date(),
    };
    this.whatsappUsers.set(id, user);
    return user;
  }

  async removeWhatsappUser(phoneNumber: string): Promise<boolean> {
    const user = Array.from(this.whatsappUsers.values()).find(u => u.phoneNumber === phoneNumber);
    if (user) {
      user.isActive = false;
      return true;
    }
    return false;
  }

  // Trading signal operations
  async getAllActiveSignals(): Promise<TradingSignal[]> {
    return Array.from(this.tradingSignals.values())
      .filter(signal => signal.isActive)
      .sort((a, b) => b.createdAt!.getTime() - a.createdAt!.getTime());
  }

  async createTradingSignal(insertSignal: InsertTradingSignal): Promise<TradingSignal> {
    const id = this.currentSignalId++;
    const signal: TradingSignal = {
      ...insertSignal,
      id,
      isActive: true,
      whatsappSent: false,
      createdAt: new Date(),
    };
    this.tradingSignals.set(id, signal);
    return signal;
  }

  async updateSignalWhatsappSent(id: number): Promise<boolean> {
    const signal = this.tradingSignals.get(id);
    if (signal) {
      signal.whatsappSent = true;
      return true;
    }
    return false;
  }

  // Portfolio operations
  async getAllPortfolioPositions(): Promise<PortfolioPosition[]> {
    return Array.from(this.portfolioPositions.values()).filter(pos => pos.isActive);
  }

  async createPortfolioPosition(insertPosition: InsertPortfolioPosition): Promise<PortfolioPosition> {
    const id = this.currentPositionId++;
    const position: PortfolioPosition = {
      ...insertPosition,
      id,
      isActive: true,
      createdAt: new Date(),
    };
    this.portfolioPositions.set(id, position);
    return position;
  }

  async updatePortfolioPosition(id: number, updates: Partial<PortfolioPosition>): Promise<PortfolioPosition | undefined> {
    const position = this.portfolioPositions.get(id);
    if (position) {
      Object.assign(position, updates);
      return position;
    }
    return undefined;
  }

  // Market data operations
  async getMarketData(symbol: string): Promise<MarketData | undefined> {
    return this.marketData.get(symbol);
  }

  async updateMarketData(insertData: InsertMarketData): Promise<MarketData> {
    const id = this.currentMarketDataId++;
    const data: MarketData = {
      ...insertData,
      id,
      lastUpdated: new Date(),
    };
    this.marketData.set(insertData.symbol, data);
    return data;
  }

  // Options chain operations
  async getOptionsChain(expiryDate: Date): Promise<OptionsChain[]> {
    return Array.from(this.optionsChain.values())
      .filter(option => option.expiryDate.getTime() === expiryDate.getTime())
      .sort((a, b) => Number(a.strikePrice) - Number(b.strikePrice));
  }

  async updateOptionsChain(insertData: InsertOptionsChain[]): Promise<OptionsChain[]> {
    const results: OptionsChain[] = [];
    
    for (const data of insertData) {
      const id = this.currentOptionsChainId++;
      const option: OptionsChain = {
        id,
        strikePrice: data.strikePrice,
        callLTP: data.callLTP || null,
        callVolume: data.callVolume || null,
        putLTP: data.putLTP || null,
        putVolume: data.putVolume || null,
        expiryDate: data.expiryDate,
        lastUpdated: new Date(),
      };
      const key = `${data.strikePrice}-${data.expiryDate.getTime()}`;
      this.optionsChain.set(key, option);
      results.push(option);
    }
    
    return results;
  }
}

export const storage = new MemStorage();
